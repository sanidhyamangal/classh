# Generated by Django 3.1.2 on 2020-11-20 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('uid',
                 models.UUIDField(default=uuid.uuid4,
                                  editable=False,
                                  primary_key=True,
                                  serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('media_url', models.URLField(blank=True, null=True)),
                ('by',
                 models.ForeignKey(
                     null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     related_name='post_by',
                     to=settings.AUTH_USER_MODEL)),
                ('likes',
                 models.ManyToManyField(related_name='likes',
                                        to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'posts',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uid',
                 models.UUIDField(default=uuid.uuid4,
                                  editable=False,
                                  primary_key=True,
                                  serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
                ('by',
                 models.ForeignKey(
                     null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     related_name='comment_by',
                     to=settings.AUTH_USER_MODEL)),
                ('post',
                 models.ForeignKey(
                     null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     to='posts.post')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
    ]