# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycon_proposals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='talkproposal',
            name='duration',
            field=models.CharField(default=b'medium', max_length=16, verbose_name='Duration', choices=[(b'short', b'Short (20 min or less)'), (b'medium', b'Medium (20 - 30 min)'), (b'long', b'Long (40 min or more)')]),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='recurring',
            field=models.PositiveSmallIntegerField(default=0, help_text='Have you given this talk before?', choices=[(1, b'Yes'), (0, b'No')]),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='tutorial',
            field=models.PositiveSmallIntegerField(default=0, help_text='Would you be interested in a speaking skill tutorial?', choices=[(1, b'Yes'), (0, b'No')]),
        ),
        migrations.AddField(
            model_name='tutorialproposal',
            name='duration',
            field=models.CharField(default=b'medium', max_length=16, verbose_name='Duration', choices=[(b'short', b'Short (20 min or less)'), (b'medium', b'Medium (20 - 30 min)'), (b'long', b'Long (40 min or more)')]),
        ),
        migrations.AddField(
            model_name='tutorialproposal',
            name='recurring',
            field=models.PositiveSmallIntegerField(default=0, help_text='Have you given this talk before?', choices=[(1, b'Yes'), (0, b'No')]),
        ),
        migrations.AddField(
            model_name='tutorialproposal',
            name='tutorial',
            field=models.PositiveSmallIntegerField(default=0, help_text='Would you be interested in a speaking skill tutorial?', choices=[(1, b'Yes'), (0, b'No')]),
        ),
    ]
