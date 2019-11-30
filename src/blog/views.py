from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from taggit.models import Tag
from .models import Post
from .forms import ShareByEmailForm
from urllib.parse import quote_plus


# ListView uses MultipleObjectMixin (therefor you can use methods like is_paginated in the template)
class PostListView(ListView):
    model = Post
    context_object_name = 'posts' # Default: object_list
    # queryset = Post.objects.all() # Default: Model.objects.all()
    # template_name = 'blog/post_list.html' # Default: <app_label>/<model_name>_list.html
    # ordering = ['-date_published'] # change the ordering here or in the model
    paginate_by = 3 # passes page_obj object into the template


def post_list(request, tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        # get the Tag object with the specific tag in the db
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'blog/post_list.html', context)


class PostDetailView(DetailView):
    # model = Post
    context_object_name = 'post' # object - default

    # this works but django advises to use get_context_data() !!!
    # self.context["name_to_use"] = "value"
    # Finally I CREATED A METHOD get_time_to_read INSIDE models.py

    # Made a custom filter tag instead of this
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = self.get_object()
    #     context['share_string'] = quote_plus(post.title)
    #     return context

    def get_object(self):
        return get_object_or_404(Post,
                    date_published__year = self.kwargs.get('year'),
                    date_published__month = self.kwargs.get('month'),
                    date_published__day = self.kwargs.get('day'),
                    slug = self.kwargs.get('post_slug'),
                    status = 'published')

# def post_detail(request, year, month, day, post_slug):
#     post = get_object_or_404(Post,  slug=post_slug,
#                                     status='published',
#                                     date_published__year=year,
#                                     date_published__month=month,
#                                     date_published__day=day)
#     context = {
#         'post': post
#     }
#     return render(request, 'blog/post_detail.html', context)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts' # object_list - default
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.published.filter(author=user).order_by('-date_published')


# post_form.html
# context_object_name = 'form' - default
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'tags', 'content']

    # override the form valid method in order to add the author - the user who is submitting the post
    def form_valid(self, form):
        cd = form.cleaned_data
        form.instance.author = self.request.user
        form.instance.status = 'published' # comment if you want to be able to check the user's posts before publishing them

        # MAKING THE SLUG UNIQUE IS NOW HANDLED IN models.py
        # form.instance.slug = slugify(cd['title'])
        # slug_is_unique = not Post.objects.filter(slug__exact=form.instance.slug).exists()
        # if slug_is_unique:
        return super().form_valid(form)
        # else:
        #     messages.error(self.request, 'Title already exists!')
        #     return self.form_invalid(form)



# post_form.html
# context_object_name = 'form' - default
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'tags', 'content']

    # override the form valid method in order to add the author - the user who is submitting the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # will be run by UserPassesTestMixin
    def test_func(self):
        post = self.get_object()
        # the current logged in user == the author of the post
        if self.request.user == post.author:
            return True
        return False


# post_confirm_delete.html
# context_object_name = 'object' - default
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        # the current logged in user == the author of the post
        if self.request.user == post.author:
            return True
        return False


# However, you can't use reverse with success_url, because then reverse is called when the module is imported, before the urls have been loaded.
# def get_success_url(self):
#     return reverse('blog:post_list')
# Overriding get_success_url is one option, but the easiest fix is to use reverse_lazy instead of reverse.


def post_share(request, pk):
    post = get_object_or_404(Post, id=pk, status='published')
    sent = False

    if request.method == 'POST':
        form = ShareByEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']}({cd['email']}) recommends you {post.title[:25]}... {post.get_time_to_read()} minutes read"

            body = f"Read '{post.title}' at {post_url}\n\n{cd['name']}'s comments:\n\n{cd['comments']}"

            send_mail(subject, body, 'mihainegrisan.cv@gmail.com', [cd['to']])
            sent = True
            messages.success(request, f"Your email was successfully sent to {cd['to']}")

            # This will call the model’s get_absolute_url() method;
            return redirect(post)
        else:
            messages.error(request, "Please check again.")
    else:
        form = ShareByEmailForm()

    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }

    return render(request, 'blog/post_share_by_email.html', context)



def about(request):
    return render(request, 'blog/about.html', {})
