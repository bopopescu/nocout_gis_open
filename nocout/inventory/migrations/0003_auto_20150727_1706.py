# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20150720_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circuitl2report',
            name='name',
            field=models.CharField(max_length=250, verbose_name=b'Name'),
        ),
    ]