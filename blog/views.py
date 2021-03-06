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
from django.db.models import Count, Q
from taggit.models import Tag
from .models import Post
from .forms import ShareByEmailForm, PostForm, CommentForm
# from pagedown.widgets import PagedownWidget
from marketing.forms import EmailSignupForm


# ListView uses MultipleObjectMixin (therefor you can use methods like is_paginated in the template)
class PostListView(ListView):
    model = Post
    context_object_name = 'posts' # Default: object_list
    # queryset = Post.objects.all() # Default: Model.objects.all()
    # template_name = 'blog/post_list.html' # Default: <app_label>/<model_name>_list.html
    # ordering = ['-date_published'] # change the ordering here or in the model
    paginate_by = 4 # passes page_obj object into the template


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    form = EmailSignupForm()

    # search posts feature
    query = request.GET.get('query')
    if query:
        query = query.strip()
        object_list = object_list.filter(
            Q(title__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
            ).distinct()
        # distinct() -> no duplicates

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
        'section': 'home',
        'form': form,
    }
    return render(request, 'blog/post_list.html', context)


class PostDetailView(DetailView):
    # model = Post
    context_object_name = 'post' # object - default

    # this works but django advises to use get_context_data() !!!
    # self.context["name_to_use"] = "value"

    # def get(self, *args, **kwargs):


    def post(self, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST or None)
        if comment_form.is_valid():
            self.post = self.get_object()

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = self.post
            # Save the comment to the database
            new_comment.save()

            messages.success(self.request, 'Submitted! Your comment is awaiting moderation')
            return redirect(self.post.get_absolute_url())
        else:
            messages.error(self.request, "Comment wasn't submitted")
            return redirect(self.post.get_absolute_url())


    def get_object(self):
        return get_object_or_404(Post,
                    date_published__year = self.kwargs.get('year'),
                    date_published__month = self.kwargs.get('month'),
                    date_published__day = self.kwargs.get('day'),
                    slug = self.kwargs.get('post_slug'),
                    status = 'published')

    def get_context_data(self, **kwargs):
        # assign the object to the view !!!
        self.post = self.get_object()

        comments = self.post.comments.filter(active=True)

        # List of similar posts
        post_tags_ids = self.post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=self.post.id)

        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-date_published')[:4]

        context = super().get_context_data(**kwargs)
        context['similar_posts'] = similar_posts
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts' # object_list - default
    paginate_by = 4

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        self.user = self.get_object()
        return Post.published.filter(author=self.user).order_by('-date_published')

    def get_context_data(self, **kwargs):
        # assign the object to the view !!!
        self.user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['author'] = self.user
        return context

# post_form.html
# context_object_name = 'form' - default
class PostCreateView(LoginRequiredMixin, CreateView):
    # form_class = PostForm #uncomment if you want to add PagedownWidget
    model = Post
    # specifie the fields in the form OR in the view
    fields = ['title', 'tags', 'content'] # 'status'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'new-post'
        return context



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
    return render(request, 'blog/about.html', {'section': 'about'})
