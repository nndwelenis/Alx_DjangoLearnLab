from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BookForm()

    return render(request, "bookshelf/form_example.html", {"form": form})


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request):
    return render(request, "bookshelf/form_example.html")


@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request):
    return render(request, "bookshelf/book_list.html")
