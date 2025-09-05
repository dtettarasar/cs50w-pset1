from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("wiki/<str:entry_title>/", views.view_entry, name="view_entry"),
    path("search/", views.search_entry, name="search_entry"),
    path("edit/<str:entry_title>/", views.edit, name="edit_entry"),
]
