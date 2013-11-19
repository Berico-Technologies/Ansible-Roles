#!/usr/bin/env python

from subprocess import call

import sys, getopt, os

try:
    opts, args = getopt.getopt(sys.argv[1:], "f:r:h:d:p:")

    forwarder  = None
    ipa_realm  = None
    fqdn       = None
    ipa_domain = None
    pswd       = None

    for opt, arg in opts:
        if opt == '-f':
            forwarder = arg.strip()
        if opt == '-r':
            ipa_realm = arg.strip()
        if opt == '-h':
            fqdn = arg.strip()
        if opt == '-d':
            ipa_domain = arg.strip()
        if opt == '-p':
            pswd = arg.strip()

    if forwarder == None or fqdn == None or pswd == None or ipa_realm == None or ipa_domain == None:
        print "Missing required parameters"
        sys.exit(1)

    touch_token = "/etc/ipa_configured"

    if not os.path.exists(touch_token):

        cmd = "ipa-server-install --setup-dns --forwarder={forwarder} -r {ipa_realm} " \
              "--hostname={fqdn} -n {ipa_domain} -a {password} -p {password} -U"\
              .format(forwarder=forwarder, ipa_realm=ipa_realm, fqdn=fqdn, ipa_domain=ipa_domain, password=pswd)

        success = call(cmd, shell=True)

        if success == 0:
            touched = call("touch " + touch_token, shell=True)
            sys.exit(touched)
        else:
            print "Unable to configure FreeIPA"
            sys.exit(1)
    else:
        print "FreeIPA already configured...No action necessary"
        sys.exit(0)


except getopt.GetoptError:
    print "Could not parse command line arguments"
    sys.exit(1)