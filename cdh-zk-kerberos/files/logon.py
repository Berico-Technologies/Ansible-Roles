#!/usr/bin/env python

#
# This is a simple shell script that will call the "ipa service-add" command iff there is not
# an existing principal found using "ipa service-find".
#

from subprocess import call
import sys, getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], "p:")
    pswd = None

    for opt, arg in opts:
        if opt == '-p':
            pswd = arg.strip()

    if pswd == None:
        print "Kerberos password for admin was not provided"
        sys.exit(1)

    success = call("echo " + pswd + " | kinit admin", shell=True)

    sys.exit(success)

except getopt.GetoptError:
    print "Could not parse command line arguments"
    sys.exit(1)