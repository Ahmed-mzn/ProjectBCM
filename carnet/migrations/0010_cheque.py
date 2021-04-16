# Generated by Django 3.1.1 on 2020-09-23 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carnet', '0009_auto_20200923_0033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('numero', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('statut', models.CharField(max_length=10)),
                ('carnet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carnet.carnetcheque')),
            ],
        ),
    ]
