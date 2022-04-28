
import base64
from django.core.files.base import ContentFile
import json
from typing import Dict, List
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db.models import *


def to_dict(self, depth=1):
    opts = self._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if f.name == "password":
            continue
        if isinstance(f, ManyToManyField):
            if self.pk is None:
                data[f.name] = []
            else:
                if depth >= 0:
                    _list = map(lambda x: to_dict(x, depth-1), f.value_from_object(
                        self))
                    data[f.name] = list(_list)
        elif isinstance(f, DateTimeField):
            val = f.value_from_object(self)
            if val:
                data[f.name] = f'{val:%Y-%m-%d %H:%M:%S}'
        elif isinstance(f, ImageField):
            val = f.value_from_object(self)
            if(val):
                data[f.name] = val.url
        else:
            data[f.name] = f.value_from_object(self)
    return data


def b_to_file(data):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]

    return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
