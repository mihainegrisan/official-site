from taggit.models import Tag
from django.db.models import Count

def posts(request):
    tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).all()
    # tags: <QuerySet [<Tag: blabla>, <Tag: change>, <Tag: climate>, <Tag: google>, <Tag: image>, <Tag: jazz>, <Tag: lalaiala>, <Tag: music>, <Tag: s>, <Tag: tables>, <Tag: test>, <Tag: try>]>

    return {
        'tags': tags
    }
