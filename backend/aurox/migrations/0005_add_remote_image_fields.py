"""Add remote URL fields for Properties images."""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aurox', '0004_savedproperty'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='image1_remote_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='properties',
            name='image2_remote_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='properties',
            name='image3_remote_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
