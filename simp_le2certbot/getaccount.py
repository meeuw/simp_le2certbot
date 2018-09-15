#!/usr/bin/env python
from __future__ import print_function
import josepy
from cryptography.hazmat.backends import default_backend
from acme import client as acme_client
from cryptography.hazmat.primitives import serialization
from acme import errors, messages
import json
import sys

def main():
    if sys.argv[1] == 'staging':
        directory = 'https://acme-staging.api.letsencrypt.org/directory'
    else:
        directory = 'https://acme-v01.api.letsencrypt.org/directory'

    key = josepy.JWKRSA(key=serialization.load_pem_private_key(
       sys.stdin.read(),
       password=None,
       backend=default_backend())
    )

    net = acme_client.ClientNetwork(key)

    client = acme_client.Client(
        directory=directory,
        key=key,
        net=net
    )

    new_reg = messages.NewRegistration.from_data(
        email=sys.argv[2]
    )

    acct = None
    try:
        regr = client.register(new_reg)
    except errors.ConflictError as e: 
        acct = e.location

    print(json.dumps({'body': {}, 'uri': acct}))
