from django.shortcuts import render, get_object_or_404
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
from .models import Post
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify


def home(request):
    posts = Post.published.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #otherwise it looks for blog/post_list.html
    context_object_name = 'posts' # object_list - default
    # ordering = ['-date_published'] # change the ordering here or in the model
    paginate_by = 4 # passes page_obj object into the template


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts' # object_list - default
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # kwargs - the query parameters
        return Post.published.filter(author=user).order_by('-date_published')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post' # object - default


# post_form.html
# context_object_name = 'form' - default
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'tags', 'content']

    # override the form valid method in order to add the author - the user who is submitting the post
    def form_valid(self, form):
        cd = form.cleaned_data
        form.instance.author = self.request.user
        form.instance.slug = slugify(cd['title'])
        form.instance.status = 'published'
        if not Post.objects.filter(slug__exact=form.instance.slug).exists():
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Title already exists!')
            return self.form_invalid(form)



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


# expects a form that asks if you're sure you want to delete the post
# post_confirm_delete.html
# context_object_name = 'object' - default
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # success_url = reverse('blog:home')
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        post = self.get_object()
        # the current logged in user == the author of the post
        if self.request.user == post.author:
            return True
        return False


# However, you can't use reverse with success_url, because then reverse is called when the module is imported, before the urls have been loaded.
# def get_success_url(self):
#     return reverse('blog:home')
# Overriding get_success_url is one option, but the easiest fix is to use reverse_lazy instead of reverse.



def about(request):
    return render(request, 'blog/about.html', {})
