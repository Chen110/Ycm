# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ycm', '0004_message_who'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='who',
            field=models.CharField(max_length=30, verbose_name='\u64cd\u4f5c\u4eba\u5458'),
        ),
    ]
