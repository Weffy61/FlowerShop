from django.shortcuts import render


def index(request):
    return render(request, 'FlowerApp/index.html')


def order(request):
    return render(request, 'FlowerApp/order.html')
