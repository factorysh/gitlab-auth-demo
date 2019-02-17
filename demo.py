#!/usr/bin/env python
import os
import urllib.parse

import requests
from authlib.specs.rfc7519 import jwt
from x5092json import x509parser

"""
cryptography module is very picky with certificates:
https://stackoverflow.com/questions/53337833/could-not-deserialize-key-data-on-decoding-jwt-python

You can extaract the public key from the PEM certificate

    openssl x509 -pubkey -noout -in cert.pem  > pubkey.pem

But x5092json can open most pem files:
https://github.com/jcrowgey/x5092json

"""


class Gitlab:
    "Gitlab server"
    def __init__(self, domain):
        self.domain = domain

    def token(self, project, action='pull', client_id='gitlab_ci',
              service='container_registry', offline_token=True):
        p = urllib.parse.quote_plus(project)

        r = requests.get(('https://{domain}/jwt/auth?'
                          'client_id={cid}'
                          '&service={service}'
                          '&offline_token={ot}'
                          '&scope={scope}').format(
            domain=self.domain,
            cid=client_id,
            service=service,
            ot='true' if offline_token else 'false',
            scope='repository:%s:%s' % (p, action)),
            auth=(os.getenv('USER'), os.getenv('TOKEN')))
        return r.json().get('token')


def public_key(path):
    "Get a PEM path, return a PEM public key"
    cert = x509parser.load_certificate(open(path, 'rb'))
    cc = x509parser.parse(cert)
    public = cc['subject_public_key_info']
    assert public['algorithm'] == 'rsaEncryption'
    assert public['key_size'] >= 2048
    return """-----BEGIN PUBLIC KEY-----
%s
-----END PUBLIC KEY-----""" % public['key']


def assert_token(raw, public="public.pem"):
    "Read token and validate it"
    pk = public_key(public)
    t = jwt.decode(raw, pk)
    h = t.header
    assert h['typ'] == 'JWT'
    assert h['alg'].startswith('RS')
    size = int(h['alg'][2:])
    assert size >= 256
    t.validate()
    return t


if __name__ == '__main__':
    import json
    g = Gitlab(os.getenv('GITLAB'))
    raw = g.token(os.getenv('PROJECT'), client_id='bob')
    print(raw)
    print()
    t = assert_token(raw, public='public.pem')
    print(json.dumps(t, indent=2))
