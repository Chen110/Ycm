# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ycm', '0003_remove_message_who'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='who',
            field=models.CharField(default='ice', max_length=10, verbose_name='\u64cd\u4f5c\u4eba\u5458'),
            preserve_default=False,
        ),
    ]
