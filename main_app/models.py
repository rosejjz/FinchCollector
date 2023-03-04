from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEAL = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.

class Toy(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.color} {self.id}"
    
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk':self.id})

class Finch(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}: ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEAL)


class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEAL,
        default=MEAL[0][0]
    )

    finch = models.ForeignKey(
        Finch,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=200)
  cat = models.ForeignKey(Finch, on_delete=models.CASCADE)

  def __str__(self):
    return f'Photo for finch_id: {self.cat_id} @{self.url}'