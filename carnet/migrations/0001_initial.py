# Generated by Django 3.1.1 on 2020-09-21 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=7)),
                ('libelle', models.CharField(max_length=100)),
                ('numOrganisation', models.CharField(max_length=3)),
            ],
        ),
    ]
