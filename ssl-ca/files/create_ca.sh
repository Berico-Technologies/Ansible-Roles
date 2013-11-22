#!/bin/bash

hr="-------------------------------------------"
br=""
strength=2048
valid=365

message="Usage:  sh create_ca.sh [certificate root directory] [country] [state] [city] [organization] [common name]"

if [ $# -ne 6 ];
then
        echo $message
        exit 2
fi

if [ $1 = "--help" ];
then
        echo $message
        exit 2
fi

rootdir=$1
country=$2
state=$3
city=$4
org=$5
cn=$6

if [ ! -d $rootdir ];
then
    echo "Certificate root directory does not exist.  Please create it before setting up the CA"
    exit 1
fi

cd $rootdir

if [ ! -d ./ca/ ];
then
    echo "Creating folder: ca/"
    mkdir ca
fi

if [ ! -d ./ca/private/ ];
then
    echo "Creating folder: ca/private/"
    mkdir ca/private
fi

if [ ! -d ./ca/certs/ ];
then
    echo "Creating folder: ca/certs/"
    mkdir ca/certs
fi

if [ ! -f ./ca/serial ];
then
    echo "Creating file: ca/serial"
    echo "01" > ca/serial
fi

if [ ! -f ./ca/index.txt ];
then
    echo "Creating file: ca/index.txt"
    touch ca/index.txt
fi

if [ ! -f "${rootdir}/ca/openssl.cnf" ];
then
    echo "openssl.cnf not present in ca directory"

    if [ -f "${rootdir}/openssl.cnf" ];
    then
        echo "Found openssl.cnf in root dir.  Copying to ca/..."
        sudo cp $rootdir/openssl.cnf $rootdir/ca/openssl.cnf
        sudo chmod a+r $rootdir/ca/openssl.cnf
    else
        echo "Could not locate openssl.cnf"
        exit 1
    fi
fi

cd ca

# This should be unnecessary.
export OPENSSL_CONF="${rootdir}/ca/openssl.cnf"

if [ -f cacert.pem ] && [ -f cacert.cer ];
then
    echo "Nothing to do, CA certs exist"
    exit 0
fi

openssl req -x509 -config openssl.cnf -newkey rsa:$strength -days $valid -out cacert.pem -outform PEM \
    -subj "/CN=MyTestCA/" -nodes
#-subj "/C=$country/ST=$state/L=$city/O=$org/CN=$cn" -nodes

openssl x509 -in cacert.pem -out cacert.cer -outform DER