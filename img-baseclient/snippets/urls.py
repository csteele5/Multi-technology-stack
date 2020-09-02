from django.urls import path

from snippets.views import (snippet_list_view, snippet_detail_view, snippet_update_view, snippet_create_view, snippet_save_view, snippet_delete_view)

app_name = 'snippets'
urlpatterns = [
    path('', snippet_list_view, name='snippet-list'),
    path('<int:id>/', snippet_detail_view, name='snippet-detail'),
    path('<int:id>/update/', snippet_update_view, name='snippet-update'),
    path('<int:id>/delete/', snippet_delete_view, name='snippet-delete'),
    path('create/', snippet_create_view, name='snippet-create'),
    path('save/', snippet_save_view, name='snippet-save'),
    ]