from django.db import models

# first model is for data ingested from github, this is the main data table
class weatherData(models.Model):
    station = models.CharField(max_length=255)
    date = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    max_temp = models.IntegerField()
    min_temp = models.IntegerField()
    precip = models.IntegerField()

class weatherStats(models.Model):
    station = models.CharField(max_length=255)
    year = models.IntegerField()
    mean_max_temp = models.IntegerField()
    mean_min_temp = models.IntegerField()
    total_precip = models.IntegerField()
