from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
'''
Defines a new model class named User that inherits from AbstractUser. 
This means the User model will have all the fields and methods of AbstractUser 
(e.g., username, password, first name, last name) but can also be customized further.
'''
class User(AbstractUser):
    email = models.EmailField(unique = True)
    #specifies that email field should be used as unique identifier for the uer instead of default 'username' field
    USERNAME_FIELD = 'email'
    # While the email and password fields are always required by default, any additional fields specified in REQUIRED_FIELDS must also be provided when creating a new user.
    REQUIRED_FIELDS = ['username']


class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'sent_requests', on_delete = models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'received_requests', on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])

    class Meta:
        unique_together = ('from_user', 'to_user')
        