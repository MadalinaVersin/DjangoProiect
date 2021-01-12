from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


# Create your views here.
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from app.forms import CommentForm
from app.models import Book,Comment,User,Author,Publisher

# def index(request):
#     return HttpResponse("Welcome to the SocialApp!")

def index(request):
    book_list = Book.objects.all()
    return render(request, 'index.html', {'book_list': book_list})

class BookListView(View):

    def get(self, request, *args, **kwargs):
        book_list = Book.objects.all()
        return render(request, 'index.html', {'book_list': book_list})

class AuthorListView(View):

    def get(self, request, *args, **kwargs):
        author_list = Author.objects.all()
        return render(request, 'authors.html', {'author_list': author_list})

class PublisherListView(View):

    def get(self, request, *args, **kwargs):
        publisher_list = Publisher.objects.all()
        return render(request, 'publishers.html', {'publisher_list': publisher_list})


def book_detail(request, pk):
    book = Book.objects.get(id=pk)
    return render(request, "book_detail.html", {"book": book})

class BookDetail(DetailView):
    model=Book
    template_name="book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
 
@login_required
def comment_create(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(id=pk)
            Comment.objects.create(
                created_by=request.user,
                book=book,
                **form.cleaned_data
            )
            return redirect(reverse_lazy("book_detail", kwargs={"pk": pk}))

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        book = Book.objects.get(id=self.kwargs['pk'])
        Comment.objects.create(
            created_by=self.request.user,
            book=book,
            **form.cleaned_data
        )
        return redirect(reverse_lazy("book_detail", kwargs={"pk": self.kwargs['pk']}))

class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['text']
    pk_url_kwarg = 'pk_comment'
    template_name = 'comment_update.html'

    def form_valid(self, form):
        comment = Comment.objects.get(pk=self.kwargs['pk_comment'])
        comment.text = form.cleaned_data['text']
        comment.save()
        return redirect(reverse_lazy("book_detail", kwargs={"pk": self.kwargs['pk']}))

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "comment_delete.html"
    model = Comment
    pk_url_kwarg = 'pk_comment'

    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk": self.kwargs['pk']})

class RegisterView(CreateView):
    template_name= 'register.html'
    form_class = UserCreationForm
    model = User

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password1'])
        return redirect('book_list')


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self):
        form = AuthenticationForm()
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            login(request, user)
            return redirect(reverse_lazy('book_list'))
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('book_list'))

