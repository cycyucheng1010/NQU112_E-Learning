# Generated by Django 4.2.3 on 2024-01-03 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_studentscores_delete_student_scores'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='word_images/')),
            ],
        ),
        migrations.CreateModel(
            name='WordSentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50, unique=True)),
                ('sentence', models.TextField()),
            ],
        ),
    ]
