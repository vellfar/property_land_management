from django.shortcuts import render
from properties.models import OwnershipTransfer
from .models import *
# Create your views here.
def index(request):
    # Get properties where the logged-in user is the owner
    properties = LandProperty.objects.filter(owner=request.user)
    
    # Prepare context to send to the template
    context = {
        'properties': properties
    }

    return render(request, 'properties/index.html', context)


def transfers(request):
    user = request.user
    # Retrieve transfers where the user is the current owner or the new owner
    property_transfers = OwnershipTransfer.objects.filter(
        models.Q(current_owner=user) | models.Q(new_owner=user)
    )

    # Prepare context for the template
    context = {
        'transfers': property_transfers
    }
    return render(request, 'properties/transfers.html', context)
