# Generated by Django 4.1.1 on 2022-09-24 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fileUpload.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='S3objects',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=fileUpload.models.update_filename, validators=[fileUpload.models.validate_file_size])),
                ('uploadTime', models.DateTimeField(auto_now_add=True)),
                ('updateTime', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(blank=True, max_length=512)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
