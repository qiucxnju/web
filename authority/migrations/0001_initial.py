# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('realname', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50)),
                ('access_level', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
