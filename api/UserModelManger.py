from django.contrib.auth.base_user import BaseUserManager


class  UserModelManger(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        # normal user -->  is_superuser = False
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) 
        user.set_password(password) 
        # extra_fields.setdefault('is_superuser', False) # or user.is_superuser = False
        # extra_fields.setdefault('is_staff', False) # the default value from model.py
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        # change the default values to become superuser:
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user