# Generated by Django 3.1.1 on 2020-09-23 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carnet', '0006_auto_20200923_0012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carnetcheque',
            old_name='agent_Creation',
            new_name='id_agent_Creation',
        ),
        migrations.RenameField(
            model_name='carnetcheque',
            old_name='agent_Emission',
            new_name='id_agent_Emission',
        ),
        migrations.RenameField(
            model_name='carnetcheque',
            old_name='agent_Impression',
            new_name='id_agent_Impression',
        ),
    ]