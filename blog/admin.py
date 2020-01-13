from django.contrib import admin
from .models import Post, Comment

# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date_published', 'status')
    list_display_links = ('slug',)
    list_editable = ('title', 'date_published')
    list_filter = ('status', 'date_created', 'date_published', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',) # the author field is displayed with a lookup widget that can scale much better than a drop-down select input when you have thousands of users.
    date_hierarchy = 'date_published'
    ordering = ('status', '-date_published')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
