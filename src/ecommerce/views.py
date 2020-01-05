from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Item,
    CartItem,
    Cart,
    Address,
    Payment,
    Coupon,
    Refund,
    UserProfile,
)
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm

import random
import string
import stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def is_valid_form(values):
    valid = True
    for field in values:
        if field == "":
            valid = False
    return valid

class CheckoutView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=self.request.user, ordered=False)
            context = {
                'form': CheckoutForm(),
                'couponform': CouponForm(),
                'cart': cart,
                'DISPLAY_COUPON_FORM': True,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True,
            )
            if shipping_address_qs.exists():
                context.update({'defaul_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True,
            )
            if billing_address_qs.exists():
                context.update({'defaul_billing_address': billing_address_qs[0]})

            return render(self.request, 'checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect('ecommerce:checkout')


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)

            if form.is_valid():

                # SHIPPING
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print('Using the default shipping address')
                    shipping_address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True,
                    )
                    if shipping_address_qs.exists():
                        shipping_address = shipping_address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, 'No default shipping address available')
                        return redirect('ecommerce:checkout')
                else:
                    print('User is enterign a new shipping address')
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    # else:
                    #     messages.info(self.request, "Please fill in the required shipping address fields.")


                # BILLING
                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print('Using the default billing address')
                    billing_address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True,
                    )
                    if billing_address_qs.exists():
                        billing_address = billing_address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, 'No default shipping address available')
                        return redirect('ecommerce:checkout')
                else:
                    # User is entering the form data
                    print('User is enterign a new billing address')
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(self.request, "Please fill in the required billing address fields.")

                payment_option = form.cleaned_data.get('payment_option')


                if payment_option == 'S':
                    return redirect('ecommerce:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('ecommerce:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, 'Invalid payment option selected')
                    return redirect('ecommerce:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")
            return redirect('ecommerce:order-summary')


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user, ordered=False)
        if cart.billing_address:
            context = {
                'cart': cart,
                'DISPLAY_COUPON_FORM': False,
            }

            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card',
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0],
                    })
            return render(self.request, 'payment.html', context)
        else:
            messages.error(self.request, "You haven't added a billing address")
            return redirect('ecommerce:checkout')

    def post(self, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)

        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            # if save:
            #     # allow to fetch cards
            #     if not userprofile.stripe_customer_id:
            #         customer = stripe.Customer.create(
            #             email=self.request.user.email,
            #             source=token,
            #         )
            #         userprofile.stripe_customer_id = customer['id']
            #         userprofile.one_click_purchasing = True
            #         userprofile.save()
            #     else:
            #         # if the userprofile does already exist
            #         stripe.Customer.create_source(
            #             userprofile.stripe_customer_id,
            #             source=token
            #         )

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.create_source(
                        userprofile.stripe_customer_id,
                        source=token,
                    )
                    # customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                        source=token,
                    )
                    # customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(cart.get_total() * 100)

            try:
                if use_default:
                    intent = stripe.PaymentIntent.create(
                        amount=amount, # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id,
                    )
                else:
                    intent = stripe.PaymentIntent.create(
                        amount=amount, # cents
                        currency="usd",
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
                cart.ref_code = create_ref_code()
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


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'item' #object


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


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect('ecommerce:checkout')



class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                cart = Cart.objects.get(user=self.request.user, ordered=False)
                cart.coupon = get_coupon(self.request, code)
                cart.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect('ecommerce:checkout')
            except ObjectDoesNotExist:
                messages.info(self.request, "You don't have an active order")
                return redirect('ecommerce:checkout')


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        context = {
            'form': RefundForm(),
        }
        return render(self.request, 'request_refund.html', context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')

            # edit the order
            try:
                cart = Cart.objects.get(ref_code=ref_code)
                cart.refund_requested = True
                cart.save()

                # store the refund
                refund = Refund()
                refund.order = cart
                refund.reason = message
                refund.email = email
                refund.save()

                messages.success(self.request, "Your request was received")
                return redirect('ecommerce:request-refund')

            except ObjectDoesNotExist:
                messages.error(self.request, "This order does not exist!")
                return redirect('ecommerce:request-refund')
