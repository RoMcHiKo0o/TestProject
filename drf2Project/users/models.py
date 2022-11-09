from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

base_categories = ["Забота о себе",
                   "Зарплата",
                   "Здоровье и фитнес",
                   'Кафе и рестораны',
                   "Машина",
                   "Образование",
                   "Отдых и развлечения",
                   "Платежи, комиссии",
                   "Покупки: одежда, техника",
                   "Продукты",
                   "Проезд"]


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if email is None:
            raise TypeError("Email is required")
        if username is None:
            raise TypeError("Name is required")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.is_active = True
        user.is_superuser = False
        user.save(using=self._db)
        for category in base_categories:
            Category.objects.create(user=user, category=category)
        UserProfile.objects.create(user=user)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    objects = UserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=40)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category
