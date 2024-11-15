from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import io
import urllib, base64
import matplotlib.pyplot as plt
from django.http import HttpResponse

# @login_required(login_url='login')
def index(request):
    if request.user.is_authenticated:
        # return redirect('dashboard')
        # Example data for the plot
        # user_id = request.user.id
        # LandProperty.objects.filter(owner=user_id)
        x = [1, 2, 3, 4, 5]
        y = [10, 20, 25, 30, 35]

        # Create the plot
        plt.figure(figsize=(6, 4))
        plt.plot(x, y, marker='o')
        plt.title('Sample Plot')
        plt.xlabel('X Axis')
        plt.ylabel('Y Axis')

        # Save the plot to a memory buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Encode the plot as base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        # Pass the base64 string to the template
        return render(request, 'users/home.html', {'chart': image_base64})
    else:
        return render(request, 'templates/landing.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = request.POST['role']  # Assign role based on form input
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')

def profile(request):
    return render(request, 'users/profile.html')

def settings(request):
    return render(request, 'users/settings.html')

def updateAccount(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        return redirect('profile')
    else:
        return HttpResponse('Invalid request method')
                            
def updatePassword(request):
    if request.method == 'POST':
        user = request.user
        user.set_password(request.POST['password'])
        user.save()
        return redirect('profile')
    else:
        return HttpResponse('Invalid request method')
