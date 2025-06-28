from django.db import models
from users.models import User  


class PatientManager(models.Manager):
    def validate_patient(self, postData):
        errors = {}
        if not postData.get('name') or len(postData['name']) < 2:
            errors['name'] = "Name is required and must be at least 2 characters."
        if not postData.get('age') or not postData['age'].isdigit() or int(postData['age']) <= 0:
            errors['age'] = "Age must be a positive number."
        if postData.get('gender') not in ['Male', 'Female']:
            errors['gender'] = "Gender must be Male or Female."
        return errors

class Patient(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    medical_notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='patients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PatientManager()


class VitalManager(models.Manager):
    def validate_vitals(self, postData):
        errors = {}
        if not postData.get('blood_pressure') or '/' not in postData['blood_pressure']:
            errors['blood_pressure'] = "Blood pressure must be in format e.g. 120/80."
        if not postData.get('heart_rate') or not postData['heart_rate'].isdigit():
            errors['heart_rate'] = "Heart rate must be a number."
        if not postData.get('temperature'):
            errors['temperature'] = "Temperature is required."
        else:
            try:
                temp = float(postData['temperature'])
                if temp < 34 or temp > 43:
                    errors['temperature'] = "Temperature must be between 34°C and 43°C."
            except:
                errors['temperature'] = "Temperature must be a valid number."
        if not postData.get('oxygen_saturation') or not postData['oxygen_saturation'].isdigit():
            errors['oxygen_saturation'] = "Oxygen saturation must be a number."
        return errors

class Vital(models.Model):
    patient = models.ForeignKey(Patient, related_name='vitals', on_delete=models.CASCADE)
    blood_pressure = models.CharField(max_length=20)
    heart_rate = models.IntegerField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    oxygen_saturation = models.IntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    objects = VitalManager()
