# Generated by Django 4.2.6 on 2023-11-07 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tutors", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tutorprofile",
            old_name="tutor",
            new_name="user",
        ),
        migrations.AlterUniqueTogether(
            name="pricelist",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="tutorprofile",
            name="price_list",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="tutors.pricelist",
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="pricelist",
            name="subject",
        ),
        migrations.RemoveField(
            model_name="pricelist",
            name="tutor",
        ),
    ]