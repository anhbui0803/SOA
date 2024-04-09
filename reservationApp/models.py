from re import I
from unicodedata import category
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from more_itertools import quantify
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Location(models.Model):
    location = models.CharField(max_length=250)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location

class Bus(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True, null=True)
    bus_number = models.CharField(max_length=250)
    seats = models.FloatField(max_length=5, default=0)
    license_plate = models.CharField(max_length=250)
    brand_id = models.CharField(max_length=250)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_number
    
class BusBrand(models.Model):
    brand_name = models.CharField(max_length=250)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand_name

class Schedule(models.Model):
    code = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    depart = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='depart_location')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='destination')
    brand = models.ForeignKey(BusBrand, on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    fare = models.FloatField()
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Cancelled')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code + ' - ' + self.bus.bus_number)

    def count_available(self):
        booked = Booking.objects.filter(schedule=self).aggregate(Sum('seats'))['seats__sum'] or 0
        return self.bus.seats - booked

class Booking(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE, blank=True, null=True)
    pay_type = models.CharField(max_length=2, choices=(('1','Cash'),('2','Card')), default=1)
    total_price = models.FloatField()
    seats = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=2, choices=(('1','Pending'),('2','Paid')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code + ' - ' + self.name)

    def total_payable(self):
        return self.seats * self.schedule.fare

    
class Group(models.Model):
    name = models.CharField(max_length=100)
    discount = models.FloatField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def customers_count(self):
        return self.customers.count()


class Customer(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    dob = models.DateField()
    identity = models.CharField(max_length=250)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name