from django.core.management.base import BaseCommand
from taggit.models import Tag
import os


class Command(BaseCommand):
    help = 'Removing all tags without objects.'

    def handle(self, *args, **kwargs):
        for tag in Tag.objects.all():
            if tag.taggit_taggeditem_items.count() == 0:
                self.stdout.write(self.style.ERROR(f"Removing: {tag}"))
                tag.delete()
            else:
                self.stdout.write(self.style.SUCCESS(f"Keeping: {tag}"))
