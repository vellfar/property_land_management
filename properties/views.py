from django.shortcuts import render
from properties.models import OwnershipTransfer
from .models import *
# Create your views here.
def index(request):
    properties = LandProperty.objects.all()
    return render(request, 'properties/index.html',{'properties': properties})

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
