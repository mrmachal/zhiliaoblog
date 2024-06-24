from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/detail/<blog_id>', views.blog_detail, name='blog_detail'),
    path('blog/pub', views.public_blog, name='public_blog'),
    path('blog/comment/pub', views.pub_comment, name='pub_comment'),
    path('search', views.search, name='search'),

]
