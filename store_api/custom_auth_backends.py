from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        '''
        Synchronizes the profile model last_login/date_joined fields with the user
        model last_login/date_joined fields
        '''
        user = super().authenticate(request, username, password, **kwargs)

        if user:
            # Update the last_login and date_joined fields in the profile model
            user.profile.last_login = user.last_login
            user.profile.date_joined = user.date_joined
            user.profile.save()

        return user
