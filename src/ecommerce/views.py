from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, CartItem, Cart, BillingAddress
from .forms import CheckoutForm

def products(request):
    context = {
        'items': Item.objects.all(),
    }
    return render(request, 'products.html', context)


class CheckoutView(View):

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form,
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)

            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionality for these fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add a redirect to the selected payment option
                return redirect('ecommerce:checkout')

            messages.warning(self.request, 'Failed checkout')
            return redirect('ecommerce:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order.")
            return redirect('ecommerce:order-summary')



class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items' #object_list
    paginate_by = 1



class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order.")
            return redirect('/ecommerce/')


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'item' #object


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_item, created = CartItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False) # returns a tuple

    cart_qs = Cart.objects.filter(user=request.user, ordered=False)

    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the cart item is in the cart
        if cart.items.filter(item__slug=item.slug).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, "The item's quantity was updated")
            return redirect('ecommerce:order-summary')
        else:
            messages.info(request, 'The item was added to your cart')
            cart.items.add(cart_item)
            return redirect('ecommerce:order-summary')
    else:
        ordered_date = timezone.now()
        cart = Cart.objects.create(user=request.user, ordered_date=ordered_date)
        cart.items.add(cart_item)
        messages.info(request, 'The item was added to your cart')
        return redirect('ecommerce:order-summary')


# Remove the item from cart altogether (even if the quantity is more than 1)
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    cart_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )

    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the cart item is in the cart
        if cart.items.filter(item__slug=item.slug).exists():
            cart_item = CartItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            cart.items.remove(cart_item)
            messages.info(request, 'The item was removed from your cart')
            return redirect('ecommerce:order-summary')
        else:
            messages.info(request, 'The item was not in your cart')
            return redirect('ecommerce:product', slug=slug)
    else:
        messages.info(request, "You don't have an active order")
        return redirect('ecommerce:product', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    cart_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )

    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the cart item is in the cart
        if cart.items.filter(item__slug=item.slug).exists():
            cart_item = CartItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart.items.remove(cart_item)
            messages.info(request, "This item's quantity was updated")
            return redirect('ecommerce:order-summary')
        else:
            messages.info(request, 'This item was not in your cart')
            return redirect('ecommerce:product', slug=slug)
    else:
        messages.info(request, "You don't have an active order")
        return redirect('ecommerce:product', slug=slug)
