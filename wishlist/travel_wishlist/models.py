from django.db import models
from django.contrib.auth.models import User

# Create models like an ORM like pee wee
# The class is the table and the attributes are the columns
# To update or create tables, implement command python manage.py makemigrations
# and python manage.py migrate in the terminal
class Place(models.Model):
    #fk from the user table built in django auth system
    user = models.ForeignKey('auth.User', null = False, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    #Specifies directory to upload photo from user.
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        #If there is a photo, return the URL of the photo, otherwise return 'No photo'
        photo_str = self.photo.url if self.photo else 'No photo'
        notes_str = self.notes[100:] if self.notes else 'No notes'
        return f'{self.pk}: {self.name} Visited? {self.visited} on {self.date_visited}. Notes: {notes_str}.\nPhoto {photo_str}'
