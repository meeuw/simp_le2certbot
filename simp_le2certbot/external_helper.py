#!/usr/bin/env python
import sys
import os

def main():
    os.umask(0077)

    persisted = [
        'account_key',
        'key',
        'cert',
        'chain',
    ]
    if len(sys.argv) > 1:
        command = sys.argv[1]
        hostNames = sys.argv[2:]
    else:
        command = ''
        loadBalancerId = None

    if command == "save":
        i = -1
        result = {}
        fullchain = sys.stdin.read()
        with open("fullchain.pem", "w") as f:
            f.write(fullchain)
        for line in fullchain.split('\n'):
            if line.startswith('-----BEGIN'):
                i += 1
            if not persisted[i] in result:
                result[persisted[i]] = ''
            result[persisted[i]] += line+'\n'
    elif command == "load":
        fullchain = "fullchain.pem"
        if os.path.exists(fullchain):
            with open(fullchain) as f:
                print f.read()
    elif command == "persisted":
        print " ".join(persisted)
