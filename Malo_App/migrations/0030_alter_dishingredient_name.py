# Generated by Django 4.2 on 2023-05-25 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Malo_App', '0029_rename_exp_employers_invoice_exp_employees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishingredient',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Malo_App.ingredient'),
        ),
    ]
