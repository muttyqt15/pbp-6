from django.urls import path
from api.news.views import show_main, owner_panel, show_berita_json, add_berita_ajax, show_berita_by_owner, edit_berita, delete_berita, like_berita
from django.conf import settings
from django.conf.urls.static import static


app_name = 'news'

urlpatterns = [
    path("", show_main, name="show_main"),
    path("owner_panel/", owner_panel, name="owner_panel"),
    path("show_berita_json/", show_berita_json, name="show_berita_json"),
    path("show_berita_by_owner/", show_berita_by_owner, name="show_berita_by_owner"),
    path("add_berita_ajax/", add_berita_ajax, name="add_berita_ajax"),
    path("edit_berita/<str:berita_id>/", edit_berita, name="edit_berita"),
    path("delete_berita/<str:berita_id>/", delete_berita, name="delete_berita"),
    path("like_berita/<str:berita_id>/", like_berita, name="like_berita"),
    path("fdelete_berita/<str:berita_id>/", delete_berita, name="fdelete_berita"),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
