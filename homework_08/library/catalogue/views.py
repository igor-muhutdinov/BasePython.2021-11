from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalogue.forms import AuthorCreateForm, BookCreateForm
from catalogue.models import Book, Author


def index(request):
    books = Book.objects.prefetch_related('author').all()
    context = {
        'books': books,
    }
    return render(request, 'catalogue/index.html', context)


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class AuthorListView(PageTitleMixin, ListView):
    model = Author
    page_title = 'Authors list'
    context_object_name = 'authors'


class AuthorDetailView(PageTitleMixin, DetailView):
    model = Author
    page_title = 'Author detail'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.filter(author=self.kwargs['pk'])
        return context


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorCreateForm
    success_url = reverse_lazy("author_list")


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorCreateForm
    success_url = reverse_lazy("author_list")


class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy("author_list")

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(AuthorDeleteView, self).post(request, *args, **kwargs)


class BookListView(PageTitleMixin, ListView):
    model = Book
    page_title = 'Books list'
    context_object_name = 'books'


class BookDetailView(PageTitleMixin, DetailView):
    model = Book
    page_title = 'Book detail'
    context_object_name = 'book'


class BookCreateView(CreateView):
    model = Book
    form_class = BookCreateForm
    success_url = reverse_lazy("book_list")


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookCreateForm
    success_url = reverse_lazy("book_list")


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy("book_list")

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(BookDeleteView, self).post(request, *args, **kwargs)
