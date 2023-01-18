from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, role=1, password=None):
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


class Client(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": 2})
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=False)
    mobile = models.CharField(max_length=20, blank=True, null=False)
    company_name = models.CharField(max_length=250, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client_status = models.BooleanField(default=False, verbose_name="Converted")


class Contract(models.Model):
    client = models.ForeignKey(to='Client', on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    contract_status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateTimeField()


class Event(models.Model):
    contract = models.ForeignKey(to='Contract', on_delete=models.PROTECT)
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        limit_choices_to={"role": 3},
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    event_status = models.BooleanField(default=False)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(max_length=200, blank=True)
