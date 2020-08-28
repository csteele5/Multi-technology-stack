from django.urls import path

from snippets.views import (snippet_list_view,snippet_detail_view)

app_name = 'snippets'
urlpatterns = [
    path('', snippet_list_view, name='snippet-list'),
    path('<int:id>/', snippet_detail_view, name='snippet-detail'),
    # path('<int:id>/pairbuild/', pair_build_view, name='sprint-pairbuild'),
    # path('sprintpair/<int:id>/update/', pair_update_view, name='sprint-pairupdate'),
    
]

    # path('create/', article_create_view, name='article-create'),
    # path('<int:id>/update/', article_update_view, name='article-update'),
    # path('<int:id>/delete/', article_delete_view, name='article-delete'),
    # path('<int:id>/', article_detail_view, name='article-detail'),