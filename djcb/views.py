# -*- coding: utf-8 -*-

import urllib2
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from models import *


def index(request):
    return render_to_response('index.html', locals())


def makessl(request):
    domain = request.POST.get('domain')

    if not domain:
        return HttpResponse('missing domain')

    if not urllib2.urlopen('http://%s/' % domain).read():
        return HttpResponse('domain can not open')

    cmd = 'sudo certbot certonly --standalone -d %s -n' % domain

    os.system(cmd)

    cert_path = '/etc/letsencrypt/live/%s/cert.pem' % domain
    key_path = '/etc/letsencrypt/live/%s/privkey.pem' % domain

    if os.path.exists(cert_path) and os.path.exists(key_path):
        cert = open(cert_path).read()
        key = open(key_path).read()

        result = ''
        result += cert
        result += '\n==============================================\n'
        result += key

        d, created = Domain.objects.get_or_create(name=domain)
        d.cert = cert
        d.key = key
        d.save()

        return HttpResponse(result)

    return HttpResponse('Failed!')



