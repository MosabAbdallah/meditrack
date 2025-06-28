from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validate_user(self, postData):
        errors = {}
        if len(postData.get('first_name', '')) < 2:
            errors['first_name'] = "First name required"
        if len(postData.get('password', '')) < 8:
            errors['password'] = "Password must be 8+ characters"
        return errors

    def create_user(self, postData):
        hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            email=postData['email'],
            password=hashed_pw,
        )

    def authenticate(self, email, password):
        user = self.filter(email=email).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        return None

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
