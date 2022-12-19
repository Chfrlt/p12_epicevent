from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, role, password=None):
        if not username:
            raise ValueError("Entrer un nom d'utilisateur")
        if not role:
            raise ValueError("Les utilisateurs doivent être assignés un rôle")
        user = self.model(username=username,
                          role=role)
        if user.role == 1:
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
            user.set_password(password)
            user.save(using=self._db)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email):
        user = self.create_user(
            username,
            password=password,
            email=email
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser, PermissionsMixin):
    MANAGER = 1
    SALES = 2
    SUPPORT = 3

    ROLES_CHOICES = (
        (MANAGER, "Manager"),
        (SALES, "Sales"),
        (SUPPORT, 'Support')
        )

    username = models.CharField(max_length=255, unique=True,
                                null=False, blank=False)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(default=False)
    role = models.PositiveSmallIntegerField(choices=ROLES_CHOICES)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
