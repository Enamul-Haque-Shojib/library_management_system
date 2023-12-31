from django.shortcuts import render
from django.views.generic import FormView, ListView, View
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from book.models import ProfileBook
from django.contrib import messages

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
    
        user = form.save()
        login(self.request, user)
    
        return super().form_valid(form) 
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserLibraryAccountView(ListView):
    template_name = 'accounts/profile_page.html'
    

    model = ProfileBook

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profilebooklist'] = ProfileBook.objects.filter(author = self.request.user)

        return context




    

def return_book(request, id):
    profile_book = ProfileBook.objects.get(pk = id)
    request.user.account.balance = request.user.account.balance + profile_book.price
    request.user.account.save() 
    profile_book.delete()
    messages.success(request, 'You have successfully returned the book')
    return redirect('profile')

    
    
    