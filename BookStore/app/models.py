from django.db import models
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=70)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return "Author {} ".format(self.name)


class Publisher(models.Model):
    name = models.CharField(max_length=70)
    contactPhone = models.CharField(max_length=10)
    
    def __str__(self):
        return "Publisher {} has the contact {}".format(self.name, self.contactPhone)


class Book(models.Model):
    name = models.CharField(max_length=70)
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name = "books")
    publisher = models.ForeignKey(Publisher,on_delete = models.CASCADE, related_name = "publishers")

    def __str__(self):
        return "The book {} is created by {} and published by {}".format(self.name,self.author.name,self.publisher.name)

class Comment(models.Model):
    text = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} created by {} at {}".format(self.text, self.created_by.username, self.created_at)
