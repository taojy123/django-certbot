# -*- coding: utf-8 -*-

import urllib2
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from models import *

WEBROOT = '/tmp/webroot/'


def index(request):
    return render_to_response('index.html', locals())


def makessl(request):
    domain = request.POST.get('domain')

    if not domain:
        return HttpResponse('missing domain')

    if not urllib2.urlopen('http://%s/' % domain).read():
        return HttpResponse('domain can not open')

    if os.path.exists(WEBROOT):
        os.mkdir(WEBROOT)

    cmd = 'certbot certonly --webroot -n --agree-tos --email taojy123@163.com -d %s -w %s' % (domain, WEBROOT)

    os.system(cmd)

    cert_path = '/etc/letsencrypt/live/%s/fullchain.pem' % domain
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


def well_known(request, path):
    path = path.strip('/')
    path = os.path.join(WEBROOT, path)
    data = open(path).read()
    return HttpResponse(data)

