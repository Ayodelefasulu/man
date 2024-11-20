from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    # path('', views.post_list, name="post_list"),
    path('', views.PostListView.as_view(), name='post_list'),

    # This line below is replaced to make a unique slug for publication date
    # path('<int:id>/', views.post_detail, name='post_detail'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name="post_detail"
    ),
]
