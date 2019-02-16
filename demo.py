#!/usr/bin/env python
import os
import requests
import urllib.parse


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


if __name__ == '__main__':
    g = Gitlab(os.getenv('GITLAB'))
    t = g.token(os.getenv('PROJECT'))
    #, client_id=os.getenv('USER'))
    print(t)
