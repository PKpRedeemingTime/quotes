# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 18:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginRegistration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='alias',
        ),
    ]
