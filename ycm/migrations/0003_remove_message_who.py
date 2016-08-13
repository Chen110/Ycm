# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ycm', '0002_message_who'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='who',
        ),
    ]
