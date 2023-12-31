
from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:bookid>/', views.DetailBookView.as_view(), name='book_details'),
    path('borrownow/<int:bookid>/', views.borrow_now, name='borrownow'),
]
