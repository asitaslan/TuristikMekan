from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('update/', views.user_update, name="user_update"),
    path('password/', views.change_password, name="change_password"),
    path('comments/', views.comments, name="comments"),
    path('deletecomment/<int:id>', views.deletecomment, name="deletecomment"),
    path('mekans/', views.mekans, name="mekans"),
    path('addmekan/', views.addmekan, name='addmekan'),
    path('mekanedit/<int:id>', views.mekanedit, name='mekanedit'),
    path('mekandelete/<int:id>', views.mekandelete, name='mekandelete'),
    path('mekanaddimage/<int:id>', views.mekanaddimage, name='mekanaddimage'),

]