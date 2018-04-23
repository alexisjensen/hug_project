# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodTree',
            fields=[
                ('name', models.CharField(unique=True, max_length=128)),
                ('address', models.CharField(max_length=1024, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('numOfFT', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('typesOfFT', models.CharField(max_length=1024, blank=True)),
                ('neighbourhood', models.CharField(max_length=128, null=True, blank=True)),
                ('slug', models.SlugField(unique=True, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Park',
            fields=[
                ('parkId', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128, blank=True)),
                ('address', models.CharField(max_length=128, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('neighbourhood', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('approved', models.BooleanField(default=False)),
                ('picture', models.ImageField(upload_to=b'tree_photo', blank=True)),
                ('comm', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag', models.CharField(max_length=128, serialize=False, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('treeId', models.IntegerField(serialize=False, primary_key=True)),
                ('neighbourhood', models.CharField(max_length=128, blank=True)),
                ('commonName', models.CharField(max_length=128, blank=True)),
                ('diameter', models.FloatField(null=True, blank=True)),
                ('streetNumber', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('street', models.CharField(max_length=128, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('photo', models.ManyToManyField(to='hug.Photo', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('foodtree', models.ManyToManyField(to='hug.FoodTree', blank=True)),
                ('park', models.ManyToManyField(to='hug.Park', blank=True)),
                ('tree', models.ManyToManyField(to='hug.Tree', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=models.ManyToManyField(to='hug.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='park',
            name='photo',
            field=models.ManyToManyField(to='hug.Photo', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foodtree',
            name='photo',
            field=models.ManyToManyField(to='hug.Photo', blank=True),
            preserve_default=True,
        ),
    ]
