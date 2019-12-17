from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "date_joined",
        ]


class PostSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail",
    #                                            source='get_absolute_url',
    #                                            read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = '__all__'
