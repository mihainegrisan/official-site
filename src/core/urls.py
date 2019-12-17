from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework import routers

app_name = 'rest'

router = routers.DefaultRouter()
router.register('posts', views.PostView)
router.register('users', views.UserView)

urlpatterns = [
    # path('rest-auth/', include('rest_auth.urls')),
    # path('api/token/', obtain_auth_token, name='obtain-token'),

    path('', include(router.urls)),

    # path('', views.PostView.as_view(), name='test'),
    # path('create/', views.PostCreateView.as_view(), name='create'),
    # path('list-create/', views.PostListCreateView.as_view(), name='list-create'),
]
