#!/usr/bin/env python

#
# This is a simple shell script that will call the "ipa service-add" command iff there is not
# an existing principal found using "ipa service-find".
# ipa-getkeytab -s kdc.openampere.com -p zookeeper/kdc.openampere.com -k /etc/zookeeper/conf/krb5.keytab

from subprocess import call

import sys, getopt, os

try:
    opts, args = getopt.getopt(sys.argv[1:], "k:p:f:")

    kdc       = None
    principal = None
    krbfile   = None

    for opt, arg in opts:
        if opt == '-k':
            kdc = arg.strip()
        if opt == '-p':
            principal = arg.strip()
        if opt == '-f':
            krbfile = arg.strip()

    if kdc == None or principal == None or krbfile == None:
        print "KDC, service principal, or Keytab location not specified."
        sys.exit(1)

    if not os.path.exists(krbfile):
        success = call("ipa-getkeytab -s " + kdc + " -p " + principal + " -k " + krbfile, shell=True)

        if success == 0:
            print "Keytab successfully created."
            sys.exit(0)
        else:
            print "Could not create keytab."
            sys.exit(1)
    else:
        print "Keytab already exists...No action necessary."
        sys.exit(0)

except getopt.GetoptError:
    print "Could not parse command line arguments"
    sys.exit(1)