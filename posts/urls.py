from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('',views.index, name="index"),
    path('create/',views.create, name="create"),
    path('hashtags/<int:id>/',views.hashtags, name="hashtags"),
    path('<int:id>/like_post/',views.like_post, name="like_post"),
    path('<int:id>/comment-create/',views.comment_create, name="comment_create"),
    path('<int:post_id>/like-comments/<int:comment_id>',views.like_comments, name="like_comments"),

    path('<int:id>/delete/',views.delete, name="delete"),
    path('<int:id>/update/',views.update, name="update"),
]
