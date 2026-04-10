from django.db import models

# User Model
class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    allergies = models.TextField(blank=True, null=True)
    body_type = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Ingredient Model
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    properties = models.TextField()
    risk_factor = models.CharField(max_length=50)
    adult_dosage = models.CharField(max_length=100)
    child_dosage = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Remedy Model
class Remedy(models.Model):
    title = models.CharField(max_length=100)
    symptoms = models.TextField()
    preparation = models.TextField()
    safety_score = models.IntegerField()

    def __str__(self):
        return self.title
    


class SymptomHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptom = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class HerbProfile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    herb_name = models.CharField(max_length=100)
    score = models.IntegerField(default=50)
    feedback = models.IntegerField(default=0)
    last_used = models.DateTimeField(auto_now=True)