from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
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
    
    #*args, **kwargs are used to allow the method to accept any number of positional and keyword arguments.
    #override the save method to delete the old photo from user_images folder
    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo: 
                self.delete_photo(old_place.photo) 
        #OG save method.
        super().save(*args, **kwargs)  
    
    #deletes photo from user_images folder if it exists.    
    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)
    
    #Override delete method to delete place from db, including photo deletion        
    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)
        super().delete(*args, **kwargs)
        
    def __str__(self):
        #If there is a photo, return the URL of the photo, otherwise return 'No photo'
        photo_str = self.photo.url if self.photo else 'No photo'
        notes_str = self.notes[100:] if self.notes else 'No notes'
        return f'{self.pk}: {self.name} Visited? {self.visited} on {self.date_visited}. Notes: {notes_str}.\nPhoto {photo_str}'
