from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number):
        user = self.model(first_name=first_name, last_name=last_name,
                          email=email, phone_number=phone_number)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, password):
        user = self.create_user(first_name, last_name, email, phone_number)
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
