# Generated by Django 4.2.3 on 2023-08-10 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['publish_date']},
        ),
    ]
