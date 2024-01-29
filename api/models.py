from django.db import models

# first model is for summary stats
class weatherStats(models.Model):
    id = models.AutoField(primary_key=True)
    station = models.CharField(max_length=255)
    year = models.IntegerField()
    max_temp_mean = models.IntegerField()
    min_temp_mean = models.IntegerField()
    total_precip = models.IntegerField()

# second model is for data ingested from github, this is the main data table
class weatherData(models.Model):
    id = models.AutoField(primary_key=True)
    station = models.CharField(max_length=255)
    date = models.IntegerField()
    year = models.IntegerField()
    max_temp = models.IntegerField()
    min_temp = models.IntegerField()
    precip = models.IntegerField()
    

