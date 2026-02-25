from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('enrollment_number', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='students', to='schools.school')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
                'indexes': [models.Index(fields=['school', 'last_name', 'first_name'], name='students_st_school__f314f2_idx'), models.Index(fields=['school', 'enrollment_number'], name='students_st_school__7cab47_idx'), models.Index(fields=['school', 'email'], name='students_st_school__6fb73f_idx')],
                'constraints': [models.UniqueConstraint(fields=('school', 'email'), name='uniq_student_email_per_school'), models.UniqueConstraint(fields=('school', 'enrollment_number'), name='uniq_enrollment_per_school')],
            },
        ),
    ]
