# Generated by Django 3.1.5 on 2021-01-13 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('image', models.ImageField(upload_to='base/')),
                ('pt1', models.CharField(max_length=32)),
                ('pt2', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UnprocessedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='unprocessed/')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='processed/')),
                ('base', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='align_tap.baseimage')),
            ],
        ),
    ]
