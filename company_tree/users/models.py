from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    DecimalField,
    ManyToManyField,
    Model,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    """
    Default custom user model for company-tree.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Department(MPTTModel):
    """Department class for tree-like departments structure"""

    name = CharField(max_length=100, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Employee(Model):
    last_name = CharField(max_length=100)
    first_name = CharField(max_length=100)
    patronic_name = CharField(max_length=100, null=True, blank=True)
    employment_date = DateField(auto_now_add=True)
    employment_date.editable = True
    salary = DecimalField(max_digits=8, decimal_places=2)
    departments = ManyToManyField("Department")

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronic_name}"

    class MPTTMeta:
        order_insertion_by = ["name"]
