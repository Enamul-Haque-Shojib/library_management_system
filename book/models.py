from django.db import models
from category.models import Category  
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    bookid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'uploads', blank = True, null = True)

    def __str__(self):
        return self.title
    

class ProfileBook(models.Model):
    
    bookid = models.IntegerField()
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    borrowed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    borrowed_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'uploads', blank = True, null = True)
   

    def __str__(self):
        return self.title
    

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name= 'reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank = True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviews by {self.body}"

