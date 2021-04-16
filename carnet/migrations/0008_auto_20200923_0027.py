# Generated by Django 3.1.1 on 2020-09-23 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carnet', '0007_auto_20200923_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carnetcheque',
            name='date_Creation',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='carnetcheque',
            name='date_Emission',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='carnetcheque',
            name='date_Impression',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='carnetcheque',
            name='id_agent_Creation',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='carnetcheque',
            name='id_agent_Emission',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='carnetcheque',
            name='id_agent_Impression',
            field=models.IntegerField(default=None, null=True),
        ),
    ]