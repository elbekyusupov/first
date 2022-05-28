from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
import random, uuid, os
# from django.utils.translation import ugettext_lazy
# from ..helper.models import TimeStamp, Region
# from ..notification.models import send_sms_to_phone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        if password is None:
            raise TypeError(
                'Superuser must have a password'
            )
        user = self.create_user(email=email, password=password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


def get_avatar(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('account', filename)


class User(AbstractUser):
    CHOICE_TYPE = (
        (1, "Begin"),
        (2, "Check Sms"),
        (3, "Succes")
    )
    CHOICE_REGION = (
        (1, "Qashqadaryo"),
        (2, "Toshkent"),
        (3, "Namangan")
    )
    
    GENDER_TYPE = (
        (1, "Man"),
        (2, "Woman")
    )
    # middle_name = models.CharField(blank=True, null=True, max_length=250)
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.CharField(max_length=250, unique=True)
    # region = models.IntegerField(choices=CHOICE_REGION, default=1)
    address = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to=get_avatar, default='default__images/user.png', null=True, blank=True)
    # birthday = models.DateField(null=True, blank=True)
    # gender = models.IntegerField(choices=GENDER_TYPE, default=1)
    verified = models.IntegerField(choices=CHOICE_TYPE, default=1)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # code = models.CharField(max_length=10, null=True, blank=True)
    # firebase_token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = ['last_name', 'first_name', 'username']

    def __str__(self):
        return 'User — ' + self.email

    # def save(self, *args, **kwargs):
    #     if self.code is None:
    #         self.code = generate_code(self.phone)
    #     super().save()


# def generate_code(phone):
#     if phone:
#         code = random.randint(9999, 99999)
#         return code
#     return False


# def verification_code_saver(sender, instance, **kwargs):
#     if kwargs['created']:
#         phone = instance.phone
#         code = instance.code
#         send_sms_to_phone(phone, 'Tasdiqlash kodi: '+str(code))


# post_save.connect(receiver=verification_code_saver, sender=User)