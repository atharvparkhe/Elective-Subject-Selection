# Generated by Django 4.2.2 on 2023-07-05 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_changeelectivemodel_teacher_1_approval_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changeelectivemodel',
            name='is_resolved',
        ),
        migrations.AddField(
            model_name='changeelectivemodel',
            name='final_decision',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default=('PENDING', 'PENDING'), max_length=10),
        ),
    ]