from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='main'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('authors/update/<int:pk>/', views.AuthorUpdateView.as_view(), name='author_update'),
    path('authors/delete/<int:pk>/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book_delete'),
]
