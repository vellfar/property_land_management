from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from properties.models import OwnershipTransfer
from .models import *
from .forms import LandPropertyForm, PropertyForm, LocationForm
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


def add_property(request):
    if request.method == "POST":
        # Initialize the form with POST data
        property_form = PropertyForm(request.POST)
        location_form = LocationForm(request.POST)

        if property_form.is_valid() and location_form.is_valid():
            # Save location data first
            location = location_form.save()

            # Save property data with the location
            property = property_form.save(commit=False)
            property.location = location
            property.owner = request.user  # Set the owner to the logged-in user
            property.added_by = request.user  # Set the user adding the property
            property.save()

            # Redirect to a success page or the owner's dashboard
            return redirect('dashboard')  # Replace 'dashboard' with your actual URL name

    else:
        property_form = PropertyForm()
        location_form = LocationForm()

    return render(request, 'properties/add_property.html', {
        'property_form': property_form,
        'location_form': location_form
    })

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