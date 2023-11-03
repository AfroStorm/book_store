from django.contrib.auth.backends import ModelBackend


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)

        if user:
            '''
            Synchronizes the last_login and date_joined fields of the
            user model with the corresponding fields of the profile model
            '''
            user.profile.last_login = user.last_login
            user.profile.save()

        return user
