# Generated by Django 2.1.4 on 2018-12-22 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20181222_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='trailer',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
