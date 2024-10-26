from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from .forms import AuthorForm,BookForm
from .models import Book
from django import forms
# Create your views here.


def createBook(request):
    books = Book.objects.all()

    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        print(form)

        if form.is_valid():
           form.save()

           return redirect('/')
    else:
        form = BookForm()

    return render(request,'admin/book.html',{'form':form ,'books':books})

def Create_Author(request):
    if request.method== 'POST':
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form = AuthorForm()
        return render(request,'admin/author.html',{'form':form})


def listbook(request):
    books = Book.objects.all()
    paginator = Paginator(books,4)
    page_number=request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)

    return render(request,'admin/listbook.html',{'books':books,'page':page})

def detailsview(request,book_id):
    book = Book.objects.get(id=book_id)
    return render(request,'admin/detailsview.html',{'book':book})

def updateBook(request,book_id):
    book = Book.objects.get(id=book_id)

    if request.method== "POST":
        form = BookForm(request.POST,request.FILES,instance=book)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = BookForm(instance=book)
        return render(request,'admin/updateview.html',{'form':form})


def deleteview(request,book_id):
    book=Book.objects.get(id=book_id)

    if request.method== "POST":
        book.delete()
        return redirect('/')
    return render(request,'admin/deleteview.html',{'book':book})

def index(request):
    return render(request,'admin/base.html')

def search_book(request):
    query=None
    books=None
    if 'q' in request.GET:
         query=request.GET.get('q')
         books = Book.objects.filter(Q(title__icontains=query))
    else:
        books=[]
    context={'books': books,'query':query}
    return render(request,'admin/search.html',context)




