from django.db import models

# Create models like an ORM like pee wee
# The class is the table and the attributes are the columns
# To update or create tables, implement command python manage.py makemigrations
# and python manage.py migrate in the terminal
class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} Visited? {self.visited} '
