#!/bin/sh
# Kurz-Anruf beim N950: alter OpenSSH, eigener Schluessel.
#   tools/n950.sh "<befehl>"
exec ssh -o ConnectTimeout=20 -o HostKeyAlgorithms=+ssh-rsa \
     -o PubkeyAcceptedKeyTypes=+ssh-rsa -i "$HOME/.ssh/id_rsa_n9" \
     user@192.168.1.8 "$@"
