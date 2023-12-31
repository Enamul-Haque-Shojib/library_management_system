
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView,UserLibraryAccountView, return_book
from book.views import DetailBookView
 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserLibraryAccountView.as_view(), name='profile' ),
    path('details/<int:bookid>/', DetailBookView.as_view(), name='profilebook_details'),
    path('return/<int:id>/', return_book, name='returnbook'),
]