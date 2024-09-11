from django.urls import path
from . import views
from .views import (
    ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView, CategoryListView,
    TagCreateView, TagUpdateView, TagDeleteView, TagListView,
    CommentCreateView, CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    path('', views.ArticleListeViews.as_view(), name='article_list'),
    path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),

    # URLs pour Category
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/new/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # URLs pour Tag
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/new/', TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/edit/', TagUpdateView.as_view(), name='tag_update'),
    path('tags/<int:pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),

    # Commentaire
    path('article/<int:article_id>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:comment_id>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
