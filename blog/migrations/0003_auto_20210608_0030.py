# Generated by Django 3.2.3 on 2021-06-07 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210604_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='nftimagefile',
            field=models.ImageField(default='xyz', upload_to='uploads/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=400),
        ),
    ]