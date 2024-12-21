from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("like/<int:id>/", views.like_thread, name="like_thread"),
    path("edit/<int:id>/", views.edit_thread, name="edit_thread"),
    path("delete/<int:id>/", views.delete_thread, name="delete_thread"),
    path("like/comment/<int:comment_id>/", views.like_comment, name="like_comment"),
    path("delete/comment/<int:id>/", views.delete_comment, name="delete_comment"),
    path("<int:id>/", views.detail_thread, name="detail_thread"),
    # Flutter-specific API views
    path("fcreate/", views.fcreate_thread, name="fcreate_thread"),
    path("<int:thread_id>/flike/", views.flike_thread, name="flike_thread"),
    path("<int:thread_id>/fedit/", views.fedit_thread, name="fedit_thread"),
    path("<int:thread_id>/fdelete/", views.fdelete_thread, name="fdelete_thread"),
    path(
        "<int:thread_id>/fdetails/",
        views.fget_thread_details,
        name="fget_thread_details",
    ),
    path("<int:thread_id>/fcomment/", views.fadd_comment, name="fadd_comment"),
    path("<int:comment_id>/comment/flike/", views.flike_comment, name="flike_comment"),
    path(
        "<int:comment_id>/comment/fdelete/",
        views.fdelete_comment,
        name="fdelete_comment",
    ),
    path("fget_thread/", views.fget_thread, name="fget_thread"),
]
