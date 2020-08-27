from django.urls import path

from schedule.views import (sprint_list_view, sprint_detail_view, pair_build_view, pair_update_view)

app_name = 'schedule'
urlpatterns = [
    path('', sprint_list_view, name='sprint-list'),
    path('<int:id>/', sprint_detail_view, name='sprint-detail'),
    path('<int:id>/pairbuild/', pair_build_view, name='sprint-pairbuild'),
    path('sprintpair/<int:id>/update/', pair_update_view, name='sprint-pairupdate'),
    
]

    # path('projectteam/<int:id>/automate/', sprint_automate_view, name='sprint-automate'),
    # path('create/', article_create_view, name='article-create'),
    # path('<int:id>/update/', article_update_view, name='article-update'),
    # path('<int:id>/delete/', article_delete_view, name='article-delete'),
    # path('<int:id>/', article_detail_view, name='article-detail'),