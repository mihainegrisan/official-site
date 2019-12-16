from django.shortcuts import render, get_object_or_404
from .models import Item, CartItem, Cart
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone


def products(request):
    context = {
        'items': Item.objects.all(),
    }
    return render(request, 'ecommerce/products.html', context)


def checkout(request):
    return render(request, 'ecommerce/checkout.html')


class HomeView(ListView):
    model = Item
    template_name = 'ecommerce/home.html'
    context_object_name = 'items' #object_list

class ItemDetailView(DetailView):
    model = Item
    template_name = 'ecommerce/product.html'
    context_object_name = 'item' #object


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_item = CartItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)[0]
    cart_qs = Cart.objects.filter(user=request.user, ordered=False)

    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the cart item is in the cart
        if cart.items.filter(item__slug=item.slug).exists():
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart.items.add(cart_item)
    else:
        ordered_date = timezone.now()
        cart = Cart.objects.create(user=request.user, ordered_date=ordered_date)
        cart.items.add(cart_item)

    return redirect('ecommerce:product', slug=slug)
