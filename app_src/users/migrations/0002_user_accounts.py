# Generated by Django 4.1.6 on 2023-02-15 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='accounts',
            field=models.ManyToManyField(through='users.UserAccount', to='users.account'),
        ),
    ]
