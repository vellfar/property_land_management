from django.shortcuts import render
from properties.models import OwnershipTransfer
from .models import *
# Create your views here.
def index(request):
    properties = LandProperty.objects.all()
    return render(request, 'properties/index.html',{'properties': properties})

def transfers(request):
    user_id = request.user.id
    property_transfers = OwnershipTransfer.objects.filter(current_owner=user_id).filter(status=1 or 2)
    context = {
        'transfers': property_transfers
    }
    return render(request, 'properties/transfers.html', context)