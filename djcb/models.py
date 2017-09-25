# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class Domain(models.Model):

    name = models.CharField(max_length=255)
    cert = models.TextField(blank=True)
    key = models.TextField(blank=True)

    create_time = models.DateTimeField(default=timezone.now)
