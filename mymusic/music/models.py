from django.db import models
from django.core.validators import FileExtensionValidator



# in orm sql query runs in background for see this in cmd python manage.py sqlmigrate music 0001 here 0001 is the migrations port no
# Create your models here.
class Album(models.Model):
    title=models.CharField(max_length=100,null=False,help_text='album name')
    artist=models.CharField(max_length=100,help_text="album artist")
    genre=models.CharField(max_length=100,help_text="album genre")
    year=models.DateField(help_text="album year")
    image=models.FileField(validators=[FileExtensionValidator(['jpg','png'])],default='')
    def __str__(self):
        return self.title


class Song(models.Model):
    al_id=models.ForeignKey(Album,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,help_text='song title')
    artist=models.CharField(max_length=100,help_text='song artist')
    genre=models.CharField(max_length=20,help_text='song genre')
    sfile=models.FileField(validators=[FileExtensionValidator(['mp3','aac'])])
    image=models.FileField(validators=[FileExtensionValidator(['jpg','png'])])

    def __str__(self):
        return self.title