from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Item, CartItem, Cart
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone


def products(request):
    context = {
        'items': Item.objects.all(),
    }
    return render(request, 'products.html', context)


def checkout(request):
    return render(request, 'checkout.html')


class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items' #object_list
    paginate_by = 1

class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'item' #object


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
            messages.info(request, "This item's quantity was updated")
            return redirect('ecommerce:product', slug=slug)
        else:
            messages.info(request, 'This item was added to your cart')
            cart.items.add(cart_item)
            return redirect('ecommerce:product', slug=slug)
    else:
        ordered_date = timezone.now()
        cart = Cart.objects.create(user=request.user, ordered_date=ordered_date)
        cart.items.add(cart_item)
        messages.info(request, 'This item was added to your cart')
        return redirect('ecommerce:product', slug=slug)


# Remove the item from cart altogether (even if the quantity is more than 1)
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
            messages.info(request, 'This item was removed from your cart')
            return redirect('ecommerce:product', slug=slug)
        else:
            messages.info(request, 'This item was not in your cart')
            return redirect('ecommerce:product', slug=slug)
    else:
        messages.info(request, "You don't have an active order")
        return redirect('ecommerce:product', slug=slug)
