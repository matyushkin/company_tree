# Generated by Django 4.0.8 on 2022-11-14 16:43

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_department_parent_department_parent_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='department',
            new_name='emp_department',
        ),
        migrations.AddField(
            model_name='department',
            name='dep_employee',
            field=mptt.fields.TreeManyToManyField(blank=True, null=True, to='users.employee'),
        ),
        migrations.RemoveField(
            model_name='department',
            name='parent',
        ),
        migrations.AddField(
            model_name='department',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='users.department'),
        ),
    ]