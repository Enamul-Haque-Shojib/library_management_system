
from django.shortcuts import render, redirect
from . import forms
from . import models
from django.views.generic import DetailView
from django.contrib import messages
from django.template.defaulttags import register

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.



def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user' : user,
        'amount' : amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def check_profile_book(request, obj):
    book = models.Book.objects.get(pk = get_item(obj,'bookid'))
    
    profile_book = models.ProfileBook.objects.filter(bookid = book.bookid, title = book.title, author = request.user)
    return profile_book


class DetailBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'bookid'
    template_name = 'books/book_details.html'

    

    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data = self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit = False)
            new_review.book = book
            new_review.author = self.request.user
            new_review.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()

        review_form = forms.ReviewForm()
        
        context['reviews'] = reviews
        if self.request.user.is_authenticated:
            if check_profile_book(self.request, self.kwargs):
                context['review_form'] = review_form
        return context
    
    




def borrow_now(request, bookid):
    book = models.Book.objects.get(pk = bookid)
    check_in_profile_book = models.ProfileBook.objects.filter(bookid = book.bookid, title = book.title, author = request.user)
    
    
    if request.method == 'GET':

        if check_in_profile_book:
            messages.warning(request, 'You have already borrowed this book')
            return redirect('book_details',bookid=book.bookid)
        else:
            if request.user.account.balance > book.price:
                amount = request.user.account.balance - book.price
                profile_book = models.ProfileBook()
                profile_book.bookid = book.bookid
                profile_book.title = book.title
                profile_book.price = book.price
                profile_book.description = book.description
                profile_book.category = book.category
                profile_book.balance_after_transaction = amount
                profile_book.author = request.user
                profile_book.borrowed = True
                profile_book.image = book.image
                profile_book.save()
                book.borrowed = True
                book.save()
                request.user.account.balance = amount
                request.user.account.save()
                messages.success(request, 'You have successfully borrowed the book')
                send_transaction_email(request.user, book.price, "Borrowed Message", "books/borrowed_email.html")
                return redirect('book_details',bookid=book.bookid)
            else:
                messages.warning(request, 'Sorry! You dont have enough balance to borrow this book')


    return render(request, 'books/book_details.html', {'book' : book})
