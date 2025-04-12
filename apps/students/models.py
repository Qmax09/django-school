from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords
from simple_history.utils import update_change_reason
from ..corecode.models import StudentClass


class Student(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )
    registration_number = models.CharField(max_length=200, unique=True)
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_of_admission = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="students/passports/")
    history = HistoricalRecords()

    class Meta:
        ordering = ["surname", "firstname", "other_name"]

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name} ({self.registration_number})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self._state.adding: 
            previous = Student.objects.filter(pk=self.pk).first()
            if previous:
                changes = []
                for field in self._meta.fields:
                    field_name = field.name
                    old_value = getattr(previous, field_name, None)
                    new_value = getattr(self, field_name, None)
                    if old_value != new_value:
                        changes.append(f"{field_name}: {old_value} → {new_value}")

                if changes:
                    try:
                        update_change_reason(self, "; ".join(changes))
                    except AttributeError:
                        print("⚠ Ошибка обновления истории изменений, продолжаем сохранение.")

        super().save(*args, **kwargs)


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")

