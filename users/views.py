from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import io
import urllib, base64
import matplotlib.pyplot as plt



@login_required(login_url='login')
def index(request):

    # Example data for the plot
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
    return render(request, 'index.html', {'chart': image_base64})

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
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')
