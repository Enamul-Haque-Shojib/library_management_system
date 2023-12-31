from django.shortcuts import render
from django.views.generic import ListView
from book.models import Book
from category.models import Category
# Create your views here.


def home(request, category_slug = None):
    booklist = Book.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        booklist = Book.objects.filter(category = category)
    category = Category.objects.all()
    return render(request, 'index.html', {'booklist': booklist, 'category': category})

