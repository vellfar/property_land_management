from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'properties/index.html')

def transfers(request):
    return render(request, 'properties/transfers.html')