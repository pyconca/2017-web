from django.db import models
from django.utils.text import ugettext_lazy as _

from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class BaseModel(models.Model):
    """
    An abstract base class model that providers self-updating `created` and
    `modified` fields.
    """
    date_added = AutoCreatedField(_('date added'))
    date_updated = AutoLastModifiedField(_('date updated'))

    class Meta:
        abstract = True
