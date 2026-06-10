from django.urls import path
from . import views

app_name = 'knowledge'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('section/<slug:slug>/', views.section_detail, name='section_detail'),
    path('article/new/', views.article_create, name='article_create'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/edit/', views.article_edit, name='article_edit'),
    path('article/<slug:slug>/versions/', views.article_version_history, name='article_version_history'),
    path('article/<slug:slug>/versions/<int:version_number>/restore/',
         views.article_restore_version, name='article_restore_version'),
    path('article/<slug:slug>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('article/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('article/<slug:slug>/mark-outdated/', views.mark_article_outdated, name='mark_outdated'),
    path('changelog/', views.changelog_list, name='changelog'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/read/<int:pk>/', views.notification_read, name='notification_read'),
]
