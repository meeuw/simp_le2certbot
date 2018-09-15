#!/usr/bin/env python

# start as:
#
# - staging:
# simp_le2certbot staging email@example.com /var/www/html example.com
#
# - production:
# simp_le2certbot production email@example.com /var/www/html example.com

from cryptography.hazmat.primitives import serialization
import josepy
import hashlib
import subprocess
import os
import sys

def mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def symlink(source_link, link_name):
    if not os.path.exists(link_name):
        os.symlink(source_link, link_name)

def main():
    persisted = subprocess.check_output(["./external.sh", "persisted"])[:-1].split(' ')
    i = 0
    pems = dict(zip(persisted, [""]*len(persisted)))
    for line in subprocess.check_output(["./external.sh", "load"]).split('\n'):
        if not line: continue
        pems[persisted[i]] += line + "\n"
        if line.startswith('-----END'):
            i += 1


    openssl = subprocess.Popen(
        ['openssl', 'rsa', '-text', '-noout'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    rsapem2json = subprocess.Popen(
        ['rsapem2json'],
        stdin=openssl.stdout,
        stdout=subprocess.PIPE
    )

    openssl.stdin.write(pems['account_key'])
    private_key = rsapem2json.communicate()[0]

    k = josepy.JWK.json_loads(private_key)
    account = hashlib.md5(k.key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)).hexdigest()

    if sys.argv[1] == 'staging':
        directory_server = 'acme-staging-v02.api.letsencrypt.org'
    else:
        directory_server = 'acme-v02.api.letsencrypt.org'

    account_dir = 'certbot/accounts/{}/directory/{}'.format(directory_server, account)
    mkdir(account_dir)

    with open(account_dir + "/private_key.json", "w") as f:
        f.write(private_key)

    getaccount = subprocess.Popen(
        ['getaccount', sys.argv[1], sys.argv[2]],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    stdout, stderr = getaccount.communicate(pems['account_key'])
    with open(account_dir + '/regr.json', "w") as f:
        f.write(stdout)

    with open(account_dir + '/meta.json', "w") as f:
        f.write('{"creation_host": "lamp02", "creation_dt": "2018-08-30T09:29:57Z"}')

    archive = 'certbot/archive/' + sys.argv[4] + '/'
    mkdir(archive)
    with open(archive + 'privkey1.pem', 'w') as f: f.write(pems['key'])
    with open(archive + 'chain1.pem', 'w') as f: f.write(pems['chain'])
    with open(archive + 'cert1.pem', 'w') as f: f.write(pems['cert'])
    with open(archive + 'fullchain1.pem', 'w') as f: f.write(pems['cert'] + pems['chain'])
    mkdir('certbot/keys')
    with open('certbot/keys/0000_key-certbot.pem', 'w') as f: f.write(pems['key'])
    mkdir('certbot/renewal')
    with open('certbot/renewal/' + sys.argv[4] + '.conf', 'w') as f:
        f.write(
'''# renew_before_expiry = 30 days
version = 0.26.1
archive_dir = {cwd}/certbot/archive/{domain}
cert = {cwd}/certbot/live/{domain}/cert.pem
privkey = {cwd}/certbot/live/{domain}/privkey.pem
chain = {cwd}/certbot/live/{domain}/chain.pem
fullchain = {cwd}/certbot/live/{domain}/fullchain.pem

# Options used in the renewal process
[renewalparams]
account = {account}
work_dir = {cwd}/certbot/workdir
config_dir = {cwd}/certbot
server = https://{server}/directory
authenticator = webroot
logs_dir = {cwd}/certbot/logs
pref_challs = http-01,
webroot_path = {cwd},
[[webroot_map]]
'''.format(account=account, server=directory_server, cwd=os.getcwd(), domain=sys.argv[4]))
        for domain in sys.argv[4:]:
            f.write("{} = {}\n".format(domain, sys.argv[3]))

    mkdir('certbot/live/' + sys.argv[4] + '/')
    symlink('../../archive/' + sys.argv[4] + '/cert1.pem', 'certbot/live/' + sys.argv[4] + '/cert.pem')
    symlink('../../archive/' + sys.argv[4] + '/chain1.pem', 'certbot/live/' + sys.argv[4] + '/chain.pem')
    symlink('../../archive/' + sys.argv[4] + '/fullchain1.pem', 'certbot/live/' + sys.argv[4] + '/fullchain.pem')
    symlink('../../archive/' + sys.argv[4] + '/privkey1.pem', 'certbot/live/' + sys.argv[4] + '/privkey.pem')

    mkdir('certbot/logs/')
