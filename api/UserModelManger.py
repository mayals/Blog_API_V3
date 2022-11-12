from django.contrib.auth.base_user import BaseUserManager


class  UserModelManger(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password=None, **extra_fields):
        # normal user -->  is_superuser = False
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)      
        user = self.model(username=username, email=email, **extra_fields) 
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        # change the default values to become superuser:
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user