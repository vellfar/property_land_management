from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from properties.models import OwnershipTransfer
from .models import *
from .forms import LandPropertyForm
from django.http import HttpResponseForbidden

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



def edit_property(request, property_id):
    property = get_object_or_404(LandProperty, id=property_id)
    
    # Check if the user is the owner of the property
    if property.owner != request.user:
        return HttpResponseForbidden("You are not the owner of this property.")
    
    if request.method == "POST":
        form = LandPropertyForm(request.POST, instance=property)
        if form.is_valid():
            # Only save the name field
            property.name = form.cleaned_data['name']
            property.save()
            return redirect('properties_index')  # Redirect to property details view
    else:
        form = LandPropertyForm(instance=property)
    
    return render(request, 'properties/edit_property.html', {'form': form, 'property': property})


# View Property Details View
def view_property(request, property_id):
    property = get_object_or_404(LandProperty, id=property_id)
    return render(request, 'properties/view_property.html', {'property': property})

# Confirm Delete Property View
def confirm_delete_property(request, property_id):
    property = get_object_or_404(LandProperty, id=property_id)
    
    # Check if the user is the owner of the property
    if property.owner != request.user:
        return HttpResponseForbidden("You are not the owner of this property.")
    
    if request.method == "POST":
        # Set status to 0 (Deleted) instead of deleting from the database
        property.status = 0
        property.save()
        return redirect('properties_index')  # Redirect to the properties overview page
    
    return render(request, 'properties/confirm_delete_property.html', {'property': property})