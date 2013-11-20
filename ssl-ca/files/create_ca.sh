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
    echo "Creating folder: ca/private/"
    mkdir ca/private
    echo "Creating folder: ca/certs/"
    mkdir ca/certs
    echo "Creating folder: ca/serial"
    echo "01" > ca/serial
    echo "Creating file: ca/index.txt"
    touch ca/index.txt
fi

cd ca

if [ ! -f "${rootdir}/openssl.cnf" ];
then
    echo "openssl.cnf not present in base directory"
    exit 1
fi

export OPENSSL_CONF="${rootdir}/openssl.cnf"

if [ -f ca.key ] && [ -f cacert.pem ] && [ -f cacert.cer ];
then
    echo "Nothing to do, CA certs exist"
    exit 0
fi

openssl req -new -newkey rsa:$strength -days $valid -nodes -x509 -subj \
"/C=$country/ST=$state/L=$city/O=$org/CN=$cn" \
-keyout private/cakey.pem -out cacert.pem -outform PEM

openssl x509 -in cacert.pem -out cacert.cer -outform DER