# Generated by Django 3.2.4 on 2021-06-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForumApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='forum_image',
            field=models.ImageField(upload_to='forum_images', verbose_name='Image'),
        ),
    ]
