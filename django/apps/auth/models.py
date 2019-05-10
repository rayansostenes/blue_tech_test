import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def avatar(self):
        return f'https://i.pravatar.cc/150?u={self.username}'

    def enhance_token(self, token):
        token['isAdmin'] = self.is_staff
        token['firstName'] = self.first_name
        token['lastName'] = self.last_name
        token['email'] = self.email
        token['avatar'] = self.avatar
        token['username'] = self.username
        return token