
from django.shortcuts import render

def index(request):
    return render(request, "your_room/index.html")

def rental(request):
    return render(request, "your_room/rentals.html")