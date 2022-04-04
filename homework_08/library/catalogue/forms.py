from django.forms import ModelForm

from .models import Author, Book


class AuthorCreateForm(ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class BookCreateForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
