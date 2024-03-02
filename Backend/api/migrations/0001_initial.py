# Generated by Django 4.2.7 on 2024-01-31 15:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnglishOptional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('answer_A', models.TextField()),
                ('answer_B', models.TextField()),
                ('answer_C', models.TextField()),
                ('answer_D', models.TextField()),
                ('answer', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnglishOptionalNumber1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('topic', models.TextField()),
                ('answer_A', models.TextField()),
                ('answer_B', models.TextField()),
                ('answer_C', models.TextField()),
                ('answer_D', models.TextField()),
                ('answer', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnglishOptionalNumber2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('answer_A', models.TextField()),
                ('answer_B', models.TextField()),
                ('answer_C', models.TextField()),
                ('answer_D', models.TextField()),
                ('answer', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnglishOptionalNumber3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('answer_A', models.TextField()),
                ('answer_B', models.TextField()),
                ('answer_C', models.TextField()),
                ('answer_D', models.TextField()),
                ('answer_E', models.TextField()),
                ('answer_F', models.TextField()),
                ('answer_G', models.TextField()),
                ('answer_H', models.TextField()),
                ('answer_I', models.TextField()),
                ('answer_J', models.TextField()),
                ('answer', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnglishOptionalNumber4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('topic', models.TextField()),
                ('answer_A', models.TextField()),
                ('answer_B', models.TextField()),
                ('answer_C', models.TextField()),
                ('answer_D', models.TextField()),
                ('answer', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnglishOptionalNumber5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('topic', models.TextField()),
                ('answer_A', models.TextField()),
                ('answer_B', models.TextField()),
                ('answer_C', models.TextField()),
                ('answer_D', models.TextField()),
                ('answer', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnglishTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('topic', models.TextField()),
                ('answer_A', models.TextField()),
                ('answer_B', models.TextField()),
                ('answer_C', models.TextField()),
                ('answer_D', models.TextField()),
                ('answer', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnglishWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('part_of_speech', models.TextField()),
                ('explain', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EnglishWordSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('phonetic_symbols', models.TextField()),
                ('part_of_speech', models.TextField()),
                ('explain', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OptionalTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('topic', models.TextField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OptionalTopicNumber2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('topic', models.TextField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OptionalTopicNumber3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('topic', models.TextField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OptionalTopicNumber4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('topic', models.TextField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OptionalTopicNumber5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.TextField()),
                ('topic', models.TextField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('comments', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentScores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='WordInfos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.TextField(blank=True, null=True)),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='word_images/')),
                ('image_url', models.TextField(blank=True, null=True)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.englishword')),
            ],
        ),
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
        migrations.CreateModel(
            name='ExamPapers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('questions_optional_number1', models.ManyToManyField(to='api.englishoptionalnumber1')),
                ('questions_optional_number2', models.ManyToManyField(to='api.englishoptionalnumber2')),
                ('questions_optional_number3', models.ManyToManyField(to='api.englishoptionalnumber3')),
                ('questions_optional_number4', models.ManyToManyField(to='api.englishoptionalnumber4')),
                ('questions_optional_number5', models.ManyToManyField(to='api.englishoptionalnumber5')),
                ('questions_optionaltopic_number2', models.ManyToManyField(to='api.optionaltopicnumber2')),
                ('questions_optionaltopic_number3', models.ManyToManyField(to='api.optionaltopicnumber3')),
                ('questions_optionaltopic_number5', models.ManyToManyField(to='api.optionaltopicnumber5')),
            ],
        ),
        migrations.CreateModel(
            name='ExamPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('questions_optional_number1', models.ManyToManyField(to='api.englishoptionalnumber1')),
                ('questions_optional_number2', models.ManyToManyField(to='api.englishoptionalnumber2')),
                ('questions_optional_number3', models.ManyToManyField(to='api.englishoptionalnumber3')),
                ('questions_optional_number4', models.ManyToManyField(to='api.englishoptionalnumber4')),
                ('questions_optional_number5', models.ManyToManyField(to='api.englishoptionalnumber5')),
                ('questions_optionaltopic_number2', models.ManyToManyField(to='api.optionaltopicnumber2')),
                ('questions_optionaltopic_number3', models.ManyToManyField(to='api.optionaltopicnumber3')),
                ('questions_optionaltopic_number5', models.ManyToManyField(to='api.optionaltopicnumber5')),
            ],
        ),
    ]
