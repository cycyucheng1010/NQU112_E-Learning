# Generated by Django 4.2.3 on 2024-01-03 03:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_englishwordsearch_student_scores_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentScores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.DeleteModel(
            name='student_scores',
        ),
    ]
