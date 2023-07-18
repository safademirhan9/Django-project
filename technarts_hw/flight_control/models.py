from django.db import models

class Airline(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    callsign = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    base_airport = models.CharField(max_length=100)

class Aircraft(models.Model):
    id = models.BigAutoField(primary_key=True)
    manufacturer_serial_number = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    operator_airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    number_of_engines = models.IntegerField()

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
