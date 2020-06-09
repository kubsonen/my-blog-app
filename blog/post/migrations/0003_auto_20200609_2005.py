# Generated by Django 3.0.6 on 2020-06-09 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20200510_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='path',
            field=models.FileField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='post',
            name='postImages',
            field=models.ManyToManyField(blank=True, null=True, to='post.Images'),
        ),
    ]
