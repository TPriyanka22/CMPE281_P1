import email
from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from django.core.exceptions import ValidationError


# Create your models here.
def update_filename(instance, filename):
    old_filename, extension = os.path.splitext(filename)
    new_filename = old_filename + "_" + str(instance.id) + extension
    return new_filename


def validate_file_size(value):
    filesize = value.size
    if filesize > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value


class FileObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=update_filename, validators=[validate_file_size])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    uploadTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return os.path.basename(self.file.name)

# class Person(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=20, blank=False, null=False)
#     email = models.EmailField(blank=False, null= False)
