from django.test import TestCase
from django.urls import reverse
from .models import Place

# Create your tests here.
class TestHomePage(TestCase):

    def test_home_page_shows_empty_message_for_empty_database(self):
        
        #Arrange - Set up the test environment.
        #reverse function is used to get the URL for the view named 'place_list' defined in urls.py
        home_page_url = reverse('place_list')
        
        #Act - Perform the action that you want to test.
        response = self.client.get(home_page_url) #Simulate a GET request to the home page URL and store the response.
        
        #Assert - Check that the expected outcome has occurred.        
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') #Check that the correct template is used to render the response.
        self.assertContains(response, 'No places in the wishlist.') #Check that the response contains the text 'No places yet', which indicates that the database is empty.


