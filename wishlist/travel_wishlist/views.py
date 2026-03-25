from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

def place_list(request):
    
    if request.method == 'POST':
        #Create an instance of form with POST data
        form = NewPlaceForm(request.POST)
        place = form.save() #Save form data to create a new place object.
        if form.is_valid():
            place.save() #Save the new place to the database.
            return redirect('place_list') #Redirect to the place list page
    
    #ORM part of django, I get all the places 
    #that have not been visited from the database as a list of Place objects
    #Ex: SELECT * FROM Place WHERE visited = False ORDER BY name
    places = Place.objects.filter(visited=False).order_by('name')
    
    #Create an instance of the form base on the NewPlaceForm class defined in forms.py
    new_place_form = NewPlaceForm()
    
    # I pass a dictionary to the render function to be used in the template.
    return render(request, 'travel_wishlist/wishlist.html',
                  {'places': places, 'new_place_form': new_place_form})
    
def about(request):
    author = 'Manuel Garcia'
    about = 'Create a list of places you want to visit and mark them as visited once you have been there.'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

def places_list_visited(request):
    visited = Place.objects.filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        #Get the place object with the given primary key (place_pk) from the database. If no, return a 404 error.
        place = get_object_or_404(Place, pk=place_pk) 
        place.visited = True
        place.save()
    return redirect('places_list_visited')