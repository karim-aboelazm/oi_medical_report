# Generated by Django 4.2.13 on 2024-06-01 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("medical_report", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OurDoctors",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "doctor_name",
                    models.CharField(max_length=200, verbose_name="Doctor Name"),
                ),
                (
                    "doctor_major",
                    models.CharField(max_length=200, verbose_name="Doctor Major"),
                ),
                (
                    "doctor_image",
                    models.ImageField(
                        upload_to="doctor/images", verbose_name="Doctor Image"
                    ),
                ),
                (
                    "doctor_phone",
                    models.CharField(max_length=200, verbose_name="Doctor Phone"),
                ),
                (
                    "doctor_email",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Doctor Email",
                    ),
                ),
                (
                    "doctor_whatsapp",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Doctor Whatsapp",
                    ),
                ),
                (
                    "doctor_fb_url",
                    models.URLField(
                        blank=True, null=True, verbose_name="Doctor Facebook"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OurProjectNews",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="News Title")),
                ("description", models.TextField(verbose_name="News Description")),
            ],
        ),
        migrations.CreateModel(
            name="OurProjectNewsImages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="news/images", verbose_name="News Image"
                    ),
                ),
                (
                    "new",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medical_report.ourprojectnews",
                    ),
                ),
            ],
        ),
    ]
