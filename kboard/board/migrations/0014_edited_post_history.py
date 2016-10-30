# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-28 15:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0013_edited_post_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='editedposthistory',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='editedposthistory',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='board.Post'),
        ),
        migrations.AddField(
            model_name='editedposthistory',
            name='title',
            field=models.TextField(default=''),
        ),
    ]