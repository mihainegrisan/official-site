from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, CartItem, Cart, BillingAddress, Payment
from .forms import CheckoutForm
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


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

                if payment_option == 'S':
                    return redirect('ecommerce:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('ecommerce:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, 'Invalid payment option selected')
                    return redirect('ecommerce:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order.")
            return redirect('ecommerce:order-summary')


class PaymentView(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user, ordered=False)
        context = {
            'cart': cart,
        }
        return render(self.request, 'payment.html', context)

    def post(self, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(cart.get_total() * 100), # cents
                currency="eur",
                source=token,
            )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = intent['id']
            payment.user = self.request.user
            payment.amount = int(cart.get_total())
            payment.save()

            cart_items = cart.items.all()
            cart_items.update(ordered=True)
            for cart_item in cart_items:
                cart_item.save()

            # assign the payment to the order/cart
            cart.ordered = True
            cart.payment = payment
            cart.save()

            messages.success(self.request, "Your order was successful!")
            return redirect('ecommerce:home')

        except stripe.error.CardError as e:
            messages.error(self.request, f"{e.error.message}")
            return redirect('ecommerce:home')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit error")
            return redirect('ecommerce:home')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters")
            return redirect('ecommerce:home')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Not authenticated")
            return redirect('ecommerce:home')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network error")
            return redirect('ecommerce:home')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect('ecommerce:home')

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            # send an email to ourselves
            messages.error(self.request, "A serious error occured. We have been notified.")
            return redirect('ecommerce:home')



class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items' #object_list
    paginate_by = 10



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
