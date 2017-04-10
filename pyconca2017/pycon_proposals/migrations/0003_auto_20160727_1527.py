# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycon_proposals', '0002_auto_20160714_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talkproposal',
            name='duration',
            field=models.CharField(default=b'medium', max_length=16, verbose_name='Duration', choices=[(b'short', b'Short (~10 minutes)'), (b'medium', b'Long (~30 minutes)'), (b'long', b'Classroom tutorial (~45-60 minutes)')]),
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='recurring',
            field=models.PositiveSmallIntegerField(default=0, help_text='Have you given this talk before?', verbose_name='Previously given', choices=[(1, b'Yes'), (0, b'No')]),
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='tutorial',
            field=models.PositiveSmallIntegerField(default=0, help_text='Would you be interested in receiving mentorship / input on your talk in advance?', verbose_name='Speaker mentorship', choices=[(1, b'Yes'), (0, b'No')]),
        ),
        migrations.AlterField(
            model_name='tutorialproposal',
            name='duration',
            field=models.CharField(default=b'medium', max_length=16, verbose_name='Duration', choices=[(b'short', b'Short (~10 minutes)'), (b'medium', b'Long (~30 minutes)'), (b'long', b'Classroom tutorial (~45-60 minutes)')]),
        ),
        migrations.AlterField(
            model_name='tutorialproposal',
            name='recurring',
            field=models.PositiveSmallIntegerField(default=0, help_text='Have you given this talk before?', verbose_name='Previously given', choices=[(1, b'Yes'), (0, b'No')]),
        ),
        migrations.AlterField(
            model_name='tutorialproposal',
            name='tutorial',
            field=models.PositiveSmallIntegerField(default=0, help_text='Would you be interested in receiving mentorship / input on your talk in advance?', verbose_name='Speaker mentorship', choices=[(1, b'Yes'), (0, b'No')]),
        ),
    ]
