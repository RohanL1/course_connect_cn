# Generated by Django 4.1.7 on 2023-03-13 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribed',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscribed_subject', to='apis.subject'),
        ),
    ]
