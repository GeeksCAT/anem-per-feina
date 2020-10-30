# Generated by Django 3.0.7 on 2020-10-30 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0012_job_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='remote',
            field=models.CharField(choices=[('1', 'No remote'), ('2', 'Full remote'), ('3', 'Partial remote')], help_text='Is this job position remote?.', max_length=20, null=True, verbose_name='Remote'),
        ),
    ]