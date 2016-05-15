from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home/home.html')

def all_product(request):
    return render(request, 'home/product.html')