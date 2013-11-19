#!/usr/bin/env python

#
# This is a simple shell script that will call the "ipa service-add" command iff there is not
# an existing principal found using "ipa service-find".
#

from subprocess import call

import sys, getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], "s:f:p:r:")

    service = None
    fqdn    = None
    pswd    = None
    realm   = None

    for opt, arg in opts:
        if opt == '-s':
            service = arg.strip()
        if opt == '-f':
            fqdn = arg.strip()
        if opt == '-p':
            pswd = arg.strip()
        if opt == '-r':
            realm = arg.strip()

    if service == None or fqdn == None or pswd == None or realm == None:
        print "Service, FQDN, Kerberos password or Realm were not provided"
        sys.exit(1)

    service_exists = call("ipa service-find " + service + "/" + fqdn + "@" + realm, shell=True)

    if service_exists == 0:
        print "Principal already exists...No action necessary."
        sys.exit(0)

    try:
        call("echo " + pswd + " | kinit admin", shell=True)

    except BaseException:
        print "Could not generate Kerberos ticket!"
        sys.exit(1)

    success = call(["ipa", "service-add", service + "/" + fqdn, "--force"])

    if success == 0:
        sys.exit(0)
    else:
        print "Could not add service principal"
        sys.exit(1)

except getopt.GetoptError:
    print "Could not parse command line arguments"
    sys.exit(1)