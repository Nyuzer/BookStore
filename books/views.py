from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import ReviewForm
from django.views.generic import ListView
# from django.views.generic import DetailView
from .models import Book
from django.db.models import Q


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'book_list'
    login_url = 'account_login'


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template = 'books/book_detail.html'
    login_url = 'account_login'
    message_error = 'Something goes wrong'
    permission_required = 'books.special_status'

    def form_valid(self, form, book):
        new_comment = form.save(commit=False)
        new_comment.book = book
        new_comment.author = self.request.user
        new_comment.save()
        return redirect(reverse_lazy('book_detail', kwargs={'pk': book.id}))

    def form_invalid(self, request, form, book):
        return render(request, self.template, {'book': book, 'form': form, 'message': self.message_error})

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = ReviewForm()
        ctx = {'book': book, 'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            return self.form_valid(form, book)
        return self.form_invalid(request, form, book)


# Это пример без написания ревьюх
"""class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    login_url = 'account_login'
    permission_required = 'books.special_status'
"""


class SearchResultsListView(ListView):
    model = Book
    template_name = 'books/search_results.html'
    context_object_name = 'book_list'

    # фильтрация информации
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
