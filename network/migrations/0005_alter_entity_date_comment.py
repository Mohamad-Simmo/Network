# Generated by Django 4.0.4 on 2022-08-09 09:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_user_pfp_alter_entity_date_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 9, 9, 49, 21, 797010)),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='network.entity')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='network.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
