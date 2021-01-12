from django.contrib import admin
from . import models
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
        list_display = ('name','birthday')
        #search_fields = ('name')


class PublisherAdmin(admin.ModelAdmin):
        list_display = ('name','contactPhone')


class BookAdmin(admin.ModelAdmin):
        list_display =('name','author')
        #search_fields=('name')

class CommentAdmin(admin.ModelAdmin):
        list_display = ('text', 'created_by', 'book')

admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Publisher, PublisherAdmin)
admin.site.register(models.Book,BookAdmin)
admin.site.register(models.Comment, CommentAdmin)
