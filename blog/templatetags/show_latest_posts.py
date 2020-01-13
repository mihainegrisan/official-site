from django import template
from ..models import Post

register = template.Library()

@register.inclusion_tag('blog/latest_posts.html', name="show_latest_posts")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-date_published')[0:count]
    return {'latest_posts': latest_posts}
