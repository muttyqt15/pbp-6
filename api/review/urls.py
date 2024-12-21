from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.all_review, name='all_review'), 
    path('main/', views.main_review, name='main_review'), 
    path('create/', views.create_review, name='create_review'),
    path('edit/ajax/<uuid:id>/', views.edit_review_ajax, name='edit_review_ajax'), 
    path('delete/ajax/<uuid:id>/', views.delete_review_ajax, name='delete_review_ajax'),
    path('like/<uuid:id>/', views.like_review_ajax, name='like_review_ajax'),
    path('json/', views.show_json, name='show_json'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('flutter/create/', views.create_review_flutter, name="create_review_flutter"),
    path('flutter/user-reviews/', views.user_reviews_flutter, name='user_reviews_flutter'),
    path('flutter/<int:id>/edit/', views.edit_review_flutter, name="edit_review_flutter"),
    path('flutter/delete/<uuid:review_id>/', views.delete_review_flutter, name='delete_review_flutter'),
    path('flutter/<int:id>/like/', views.like_review_flutter, name="like_review_flutter"),
]