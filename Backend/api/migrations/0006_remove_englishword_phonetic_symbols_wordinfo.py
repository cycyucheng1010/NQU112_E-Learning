# Generated by Django 4.2.7 on 2024-01-03 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_student_scores_studentscores'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.TextField(blank=True, null=True)),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='word_images/')),
                ('image_url', models.TextField(blank=True, null=True)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.englishword')),
            ],
        ),
    ]
