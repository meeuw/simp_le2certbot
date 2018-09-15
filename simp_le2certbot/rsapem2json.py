#!/usr/bin/env python
# Usage: openssl rsa -in account_key.pem -text -noout | python rsapem2json.py
# Will convert the RSA PEM private key to the Letsencrypt/Certbot
# private_key.json file.
#
# Public Domain, Walter Doekes, OSSO B.V., 2016
#
# From:
#     -----BEGIN RSA PRIVATE KEY-----
#     MIIJJwsdAyjCseEAtNsljpkjhk9143w//jVdsfWsdf9sffLgdsf+sefdfsgE54km
#     ...
#
# To:
#     {"e": "AQAB",
#      "n": "2YIitsUxJlYn_rVn_8Sges...",
#     ...
#
from base64 import b64encode
from sys import stdin

maps = {
    'modulus': 'n', 'privateExponent': 'd', 'prime1': 'p', 'prime2': 'q',
    'coefficient': 'qi', 'exponent1': 'dp', 'exponent2': 'dq'}
extra = {'kty': 'RSA', 'e': '<publicExponent>'}

def block2b64(lines, key):
    found = False
    chars = []
    for line in lines:
        if line.startswith(key + ':'):
            found = True
        elif found and line.startswith(' '):
            for i in line.split(':'):
                i = i.strip()
                if i:
                    chars.append(chr(int(i, 16)))
        elif found:
            break
    assert chars, 'nothing found for {0}'.format(key)
    return b64encode(''.join(chars))

def main():
    data = stdin.read().split('\n')
    conv = dict((v, block2b64(data, k)) for k, v in maps.items())
    conv.update(extra)

    # Add exponent
    e = [i for i in data if i.startswith('publicExponent:')][0]
    e = e.split('(', 1)[-1].split(')', 1)[0]
    assert e.startswith('0x'), e
    e = ('', '0')[len(e) % 2 == 1] + e[2:]
    e = b64encode(''.join(chr(int(e[i:i+2], 16)) for i in range(0, len(e), 2)))
    conv['e'] = e

    # JSON-safe output.
    print(repr(conv).replace("'", '"'))
