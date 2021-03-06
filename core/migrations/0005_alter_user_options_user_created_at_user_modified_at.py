# Generated by Django 4.0.4 on 2022-06-08 17:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-created_at', '-id')},
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 6, 8, 17, 15, 42, 841776)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
