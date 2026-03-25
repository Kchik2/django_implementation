from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
@login_required
def place_list(request):
    
    if request.method == 'POST':
        #Create an instance of form with POST data
        form = NewPlaceForm(request.POST)
        #I do this because the form do not contain the user field.
        place = form.save(commit=False) #Save form data but don't commit to the database yet.
        place.user = request.user #Assign the current user to the place
        if form.is_valid():
            place.save() #Save the new place to the database.
            return redirect('place_list') #Redirect to the place list page
    
    #ORM part of django, I get all the places 
    #that have not been visited from the database as a list of Place objects
    #Ex: SELECT * FROM Place WHERE visited = False ORDER BY name
    #user=request.user filters the places to only show those that belong to the currently logged-in user. This ensures that each user sees only their own wishlist.
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    
    #Create an instance of the form base on the NewPlaceForm class defined in forms.py
    new_place_form = NewPlaceForm()
    
    # I pass a dictionary to the render function to be used in the template.
    return render(request, 'travel_wishlist/wishlist.html',
                  {'places': places, 'new_place_form': new_place_form})

@login_required    
def about(request):
    author = 'Manuel Garcia'
    about = 'Create a list of places you want to visit and mark them as visited once you have been there.'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def places_list_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        #Get the place object with the given primary key (place_pk) from the database. If no, return a 404 error.
        place = get_object_or_404(Place, pk=place_pk) 
        if place.user == request.user:
            place.visited = True #update visited field to True
            place.save() #Save updated place to the database
        else:
            return HttpResponseForbidden() #Return a 403 Forbidden response if the place does not belong to the current user.
    
    return redirect('places_list_visited')

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    return render(request, 'travel_wishlist/place_details.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.delete() #Delete the place from the database
            return redirect('place_list') #Redirect to the place list page after deletion
        else:
            return HttpResponseForbidden() #Return a 403 Forbidden response if the place does not belong to the current user.