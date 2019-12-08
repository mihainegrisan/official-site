from django.shortcuts import render
from django.conf import settings
import requests
import json
from .forms import EmailSignupForm
from .models import Signup
from django.contrib import messages
from django.http import HttpResponseRedirect

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'

members_endpoint = f'{api_url}/lists/{MAILCHIMP_EMAIL_LIST_ID}/members'

def subscribe(email):
    data = {
        'email_address': email,
        'status': 'subscribed',
    }

    r = requests.post(
        members_endpoint,
        auth=('', MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )

    return r.status_code, r.json()


def email_list_signup(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email_signup_qs = Signup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, 'You are already subscribed.')
            else:
                subscribe(form.instance.email)
                form.save()
                messages.success(request, 'Congrats! You are now subscribed to my email list!')
    # REDIRECT back to where the request was made
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
