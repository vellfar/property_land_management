from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db.models import Count, Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from io import BytesIO
from matplotlib.ticker import MaxNLocator
from properties.models import *
import urllib, base64
from .forms import UserRegistrationForm
from django.contrib.auth import update_session_auth_hash
import matplotlib.pyplot as plt
from django.contrib import messages
from django.http import HttpResponse

# @login_required
def index(request):
    if(request.user.is_authenticated):
        # 1. Get the number of properties owned by the user
        properties = LandProperty.objects.filter(owner=request.user)
        number_of_properties = properties.count()

        # 2. Get the number of active transfers involving the user
        active_transfers = OwnershipTransfer.objects.filter(
            models.Q(current_owner=request.user) | models.Q(new_owner=request.user)
        ).count()

        # 3. Calculate the total value of the user's properties (sum of valuations)
        total_property_value = properties.aggregate(total_value=Sum('valuation'))['total_value'] or 0

        # 4. Prepare data for the charts
        # Chart 1: Property value by name (Bar chart)
        property_names = properties.values_list('name', flat=True)
        property_values = properties.values_list('valuation', flat=True)

        fig1, ax1 = plt.subplots(figsize=(8, 6))
        bars = ax1.bar(property_names, property_values, color=(54/255, 162/255, 235/255, 0.6))

        # Set labels and title
        ax1.set_xlabel('Property Names')
        ax1.set_ylabel('Valuation (Millions)')
        ax1.set_title('Property Value by Name')

        # Format y-axis to show values in millions with 4 decimal places for smaller values
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: 
            "{:,.4f}M".format(x / 1e6) if x < 1e6 else "{:,.0f}M".format(x / 1e6)))

        # Set the y-axis limits based on the maximum valuation
        max_valuation = float(max(property_values)) if property_values else 0  # Convert to float if Decimal
        ax1.set_ylim(0, max_valuation * 1.1)  # Add 10% margin for better visualization

        # Add gridlines for clarity
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # Rotate the x-axis labels for better readability
        ax1.tick_params(axis='x', rotation=45)

        # Save chart to PNG
        buffer1 = BytesIO()
        plt.savefig(buffer1, format='png')
        buffer1.seek(0)
        chart1 = base64.b64encode(buffer1.getvalue()).decode()

        # Chart 2: Transfer count over months (Line chart)
        transfers = OwnershipTransfer.objects.filter(
            models.Q(current_owner=request.user) | models.Q(new_owner=request.user)
        )

        # Group by month (using request_date)
        transfer_counts = transfers.values('request_date__month').annotate(count=Count('id')).order_by('request_date__month')
        months = [str(month['request_date__month']) for month in transfer_counts]
        counts = [month['count'] for month in transfer_counts]

        # Ensure all 12 months are represented on the x-axis
        all_months = [str(i) for i in range(1, 13)]  # Months 1 to 12
        all_counts = [0] * 12  # Default counts set to 0 for all months

        for month in transfer_counts:
            month_idx = month['request_date__month'] - 1  # Convert month to 0-indexed
            all_counts[month_idx] = month['count']

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        ax2.plot(all_months, all_counts, marker='o', color=(75/255, 192/255, 192/255, 0.6))
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Number of Transfers')
        ax2.set_title('Transfers per Month')
        ax2.xaxis.set_major_locator(MaxNLocator(integer=True))  # Ensure integer values for x-axis
        ax2.set_xticks(all_months)  # Set x-ticks to represent all 12 months
        ax2.set_xticklabels([ 
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ])  # Month labels

        # Save chart to PNG
        buffer2 = BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)
        chart2 = base64.b64encode(buffer2.getvalue()).decode()

        return render(request, 'users/home.html', {
        'number_of_properties': number_of_properties,
        'active_transfers': active_transfers,
        'total_property_value': total_property_value,
        'chart1': chart1,
        'chart2': chart2
    })
    else:
        return render(request, 'templates/landing.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log in the new user
            messages.success(request, "Registration successful. Welcome!")
            return redirect('dashboard')  # Replace 'home' with your desired redirect URL
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'login_error': 'Wrong Credentials'})
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
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.nin = request.POST.get('nin')  
        user.save()
        messages.success(request, 'Account information updated successfully!')
        return redirect('settings')  
    else:
        return render(request, 'users/update_account.html', {'user': request.user})  # Pass user explicitly
    


def updatePassword(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('settings')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('settings')

        user.set_password(new_password)
        user.save()

        # Keep the user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, 'Password updated successfully!')
        return redirect('settings')
    return HttpResponse('Invalid request method', status=405)
