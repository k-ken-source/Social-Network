# Generated by Django 2.0.7 on 2021-02-14 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20210207_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='Status',
            field=models.CharField(choices=[('unlike', 'unlike'), ('like', 'like')], max_length=6),
        ),
    ]
