from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from .forms import UserForm, UserProfileForm, TourForm
from .models import UserProfile,TourPhoto,Tour
from django.contrib import auth
import logging
import plotly.graph_objects as go
from plotly.offline import plot




logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    users = User.objects.all()
    tours = Tour.objects.all()
    object_count = tours.count()

    # # graph start
    # months = []
    # dates_times = []
    # titles = []
    # hover_texts = []
    
    # for tour in tours:
    #     dates_times.append(f'{tour.date} {tour.time}')
    #     titles.append(tour.title)
    #     hover_texts.append(f'Title: {tour.title}<br>Date: {tour.date}<br>Time: {tour.time}')
    
    # fig = go.Figure()

    # months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # fig.add_shape(
    #     type="rect",
    #     x0=0, x1=1,
    #     y0=0, y1=1,
    #     xref="paper", yref="paper",
    #     fillcolor="rgba(0,0,0,0)", 
    #     layer="below"
    # )
    
   
    # fig.add_trace(go.Scatter(
    #     x=months,
    #     y=dates_times,
    #     mode='lines+markers',  
    #     text=hover_texts,
    #     marker=dict(size=8, color='red'),  
    #     line=dict(color='black', width=2),
    #     hoverinfo='text',
    #     hoverlabel=dict(bgcolor="yellow", font_size=16, font_family="Rockwell"),
    #     line_shape='spline'
    # ))

    # fig.update_layout(
    #     title='Tour Dates and Times by Month',
    #     xaxis_title='Month',
    #     yaxis_title='Date and Time',
    #     template='plotly_white',
    #     margin=dict(l=40, r=40, t=40, b=40)
    # )

    # fig.update_traces(fill='tonexty', fillcolor='rgba(15, 91, 146, 1)')


    # plot_div = plot(fig, output_type='div')

    # # graph end 

    tours1 = Tour.objects.order_by('date')

    # Prepare data for Plotly plot
    dates = [tour.date for tour in tours1]
    prices = [tour.price for tour in tours1]

    # Create Plotly figure
    fig = go.Figure(go.Scatter(x=dates, y=prices, mode='lines+markers'))

    # Customize layout if needed
    fig.update_layout(
        title='Tour Prices Over Time',
        xaxis_title='Date',
        yaxis_title='Price'
    )

    # Convert Plotly figure to JSON format
    plot_div = fig.to_json()

    # Pass the plot_div to the template for rendering
    context = {
        'plot_div': plot_div
    }



    return render(request, 'admin_dashboard.html', {'users': users , 'cou':object_count , 'plot_div':plot_div})

@login_required(login_url='login')
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    
    return render(request, 'user_dashboard.html')

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            profile_form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            return redirect('user_dashboard')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def admin_user_crud(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)
    return render(request, 'admin_user_crud.html', {'users': users})

@login_required
def create_user(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            return redirect('admin_user_crud')
    else:
        user_form = UserForm()
    return render(request, 'create_user.html', {'user_form': user_form})

@login_required
def update_user(request, user_id):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    user = get_object_or_404(User, id=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            profile_form.save()
            return redirect('admin_user_crud')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_user.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('admin_user_crud')


@login_required
def user_logout(request):
    auth.logout(request)
    return redirect("login")





# add event 
@login_required
def create_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            tour = form.save()
            
            # Handle photos separately
            files = request.FILES.getlist('photos')
            if files:
                for file in files:
                    TourPhoto.objects.create(tour=tour, photo=file)

            logger.info("Tour and photos saved successfully.")
            return redirect('tour_list') 
        else:
            logger.error("Form is invalid. Errors: %s", form.errors)
    else:
        form = TourForm()

    return render(request, 'create_tour.html', {'form': form})


@login_required
def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tour_list.html', {'tours': tours})

# user tour view 
@login_required
def user_tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'user_tour_list.html', {'tours': tours})
@login_required
def user_tour_full_view(request, pk):
    tours = get_object_or_404(Tour, pk=pk)
    return render(request, 'user_tour_full_view.html', {'tours': tours})

@login_required
def update_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            tour = form.save()

            # Handle photos separately
            files = request.FILES.getlist('photos')
            if files:
                # Delete old photos if new ones are uploaded
                TourPhoto.objects.filter(tour=tour).delete()
                for file in files:
                    TourPhoto.objects.create(tour=tour, photo=file)

            logger.info("Tour and photos updated successfully.")
            return redirect('tour_list')
        else:
            logger.error("Form is invalid. Errors: %s", form.errors)
    else:
        form = TourForm(instance=tour)
    return render(request, 'update_tour.html', {'form': form})

@login_required
def delete_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        tour.delete()
        logger.info("Tour deleted successfully.")
        return redirect('tour_list')
    return render(request, 'delete_tour.html', {'tour': tour})