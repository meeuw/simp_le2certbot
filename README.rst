====================================
simp_le to certbot migration scripts
====================================

************
Introduction
************

I've been using simp_le for some years now but it seems to be unmaintained. I've found out certbot can be used in a same way that I was using simp_le. This script converts the simp_le account configuration to certbot.

This script assumes that you're using the `external.sh` IOPlugin, I've included an example `external.sh` which expects a `fullchain.pem` file containing your account_key / certificates etc.

************************
Certbot usage as simp_le
************************

You can use the following script to use certbot like simp_le:
::

  #!/bin/bash
  CERTBOT=/var/www/certbot
  mkdir -p $CERTBOT $CERTBOT/workdir/ $CERTBOT/logs/
  certbot \
    certonly \
    --quiet \
    --agree-tos \
    --keep-until-expiring \
    --work-dir $CERTBOT/workdir/ \
    --email info@example.com \
    --webroot --webroot-path /var/www/html \
    --config-dir $CERTBOT/ \
    --logs-dir $CERTBOT/logs/ \
    --preferred-challenges=http \
    --renew-hook $CERTBOT/renew-hook.sh \
    -d example.com \
    -d www.example.com \
  #  --staging \


*****
Usage
*****

Install simp_le2certbot using the following command, I recommend using a virtualenv:

::

  $ virtualenv simp_le2certbot

  $ . simp_le2certbot/bin/activate

  $ pip install git+https://github.com/meeuw/simp_le2certbot


Next go to the directory where your `external.sh` resides, I suppose you're using this.

::

  $ cd /var/www/


Now call simp_le2certbot:

::

  $ simp_le2certbot production email@example.com /var/www/html example.com


This scripts generates a certbot directory in the format as certbot expects it to be. You can now use the above script to renew your certificates.
