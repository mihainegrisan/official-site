from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    # protocol = 'https'
    location = '/blog/'

    def items(self):
        return Post.published.all()
    # The items() method returns the QuerySet of objects to include in this sitemap. You can provide 'location' in order to specify the URL for your object. By default, location() calls get_absolute_url() on each object and returns the result(URL).
    # so go define get_absolute_url() in the Post model :)

    def lastmod(self, obj):
        return obj.date_updated

# <priority> The priority of this URL relative to other URLs on your site. Valid values range from 0.0 to 1.0. This value does not affect how your pages are compared to pages on other sites—it only lets the search engines know which pages you deem most important for the crawlers. The default priority of a page is 0.5. Please note that the priority you assign to a page is not likely to influence the position of your URLs in a search engine's result pages. Search engines may use this information when selecting between URLs on the same site, so you can use this tag to increase the likelihood that your most important pages are present in a search index.  Also, please note that assigning a high priority to all of the URLs on your site is not likely to help you. Since the priority is relative, it is only used to select between URLs on your site.
