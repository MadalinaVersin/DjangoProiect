from django.urls import path
from app.views import (
  index, 
  BookListView,
  book_detail,
  BookDetail,
  AuthorListView,
  comment_create,
  CommentCreateView,
  CommentEditView,
  CommentDeleteView,
  PublisherListView,
  RegisterView,
  LoginView,
  LogoutView,
)

urlpatterns = [
  # path('', index, name='book_list'),
  path('', BookListView.as_view(), name='book_list'),
  path('publishers', PublisherListView.as_view(), name='publisher_list'),
  path('authors', AuthorListView.as_view(), name='author_list'),
  path('register/', RegisterView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('book/<int:pk>', BookDetail.as_view(), name='book_detail'),
  path('book/<int:pk>/comment/create', comment_create, name='comment_create'),
  path('book/<int:pk>/comment/create', CommentCreateView.as_view(), name='comment_create'),
  path('book/<int:pk>/comment/<int:pk_comment>/edit', CommentEditView.as_view(), name='comment_edit'),
  path('book/<int:pk>/comment/<int:pk_comment>/delete', CommentDeleteView.as_view(), name='comment_delete'),
 ] 