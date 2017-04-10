# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycon_proposals', '0003_auto_20160727_1527'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='talkproposal',
            options={'verbose_name': 'talk proposal', 'permissions': (('can_review_unbiased', 'Can review with speaker details'),)},
        ),
    ]
