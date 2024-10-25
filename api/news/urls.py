from django.urls import path, URLResolver
from api.news.views import show_main, owner_panel, berita_entry, show_berita_json, add_berita_ajax, show_berita_by_id, show_berita_by_owner, edit_berita, delete_berita
from django.conf import settings
from django.conf.urls.static import static


app_name = 'news'

urlpatterns: list[URLResolver] = [
    path("", show_main, name="show_main"),
    path("owner_panel/", owner_panel, name="owner_panel"),
    path("show_berita_json/", show_berita_json, name="show_berita_json"),
    path("show_berita/<str:berita_id>/", show_berita_by_id, name="show_berita_by_id"),
    path("show_berita_by_owner", show_berita_by_owner, name="show_berita_by_owner"),
    path("add_berita_ajax/", add_berita_ajax, name="add_berita_ajax"),
    path("berita_entry/", berita_entry, name="berita_entry"),
    path("edit_berita/<str:berita_id>/", edit_berita, name="edit_berita"),
    path("delete_berita/<str:berita_id>/", delete_berita, name="delete_berita"),

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
