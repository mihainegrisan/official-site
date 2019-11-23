from django.contrib import admin
from .models import Post

# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date_published', 'status')
    list_filter = ('status', 'date_created', 'date_published', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',) # the author field is displayed with a lookup widget that can scale much better than a drop-down select input when you have thousands of users.
    date_hierarchy = 'date_published'
    ordering = ('status', '-date_published')
