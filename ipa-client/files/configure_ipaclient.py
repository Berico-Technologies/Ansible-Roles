#!/usr/bin/env python

from subprocess import call

import sys, getopt, os

try:
    opts, args = getopt.getopt(sys.argv[1:], "d:k:p:")

    ipa_domain = None
    kdc        = None
    pswd       = None

    for opt, arg in opts:
        if opt == '-d':
            ipa_domain = arg.strip()
        if opt == '-k':
            kdc = arg.strip()
        if opt == '-p':
            pswd = arg.strip()

    if ipa_domain == None or kdc == None or pswd == None:
        print "Missing required parameters"
        sys.exit(1)

    touch_token = "/etc/ipa_client_configured"

    if not os.path.exists(touch_token):

        cmd = "ipa-client-install --enable-dns-updates --ssh-trust-dns " \
              "--domain={ipa_domain} --server={kdc} -p admin -w {password} -U" \
              .format(ipa_domain=ipa_domain, password=pswd, kdc=kdc)

        success = call(cmd, shell=True)

        if success == 0:
            touched = call("touch " + touch_token, shell=True)
            sys.exit(touched)
        else:
            print "Unable to configure FreeIPA Client"
            sys.exit(1)
    else:
        print "FreeIPA already configured...No action necessary"
        sys.exit(0)


except getopt.GetoptError:
    print "Could not parse command line arguments"
    sys.exit(1)
    