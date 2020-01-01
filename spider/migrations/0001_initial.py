# Generated by Django 2.2.7 on 2020-01-01 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpiderReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src_type', models.IntegerField(default=0)),
                ('run_at', models.DateTimeField(auto_now=True)),
                ('crawled_pages', models.IntegerField(default=0)),
                ('running_time', models.IntegerField(default=0)),
            ],
        ),
    ]
