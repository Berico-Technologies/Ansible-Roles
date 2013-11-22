#!/bin/bash

hr="-------------------------------------------"
br=""
strength=2048
valid=365

message="Usage:  sh gen_server_cert.sh [certificate root directory] [country] [state] [city] [organization] [common name] [PKCS12 password]"

if [ $# -lt 7 ];
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
password=$7

if [ ! -d $rootdir ];
then
    echo "Certificate root directory does not exist.  Please create it before setting up the CA"
    exit 1
fi

cd $rootdir

if [ ! -f "${rootdir}/ca/openssl.cnf" ];
then
    echo "openssl.cnf not present in ca directory"
    exit 1
fi

export OPENSSL_CONF="${rootdir}/ca/openssl.cnf"

if [ ! -d ./server/ ];
then
    echo "Creating Server folder: server/"
    mkdir server
fi

cd server

file_key="${cn}.key.pem"
file_req="${cn}.req.pem"
file_cer="${cn}.cer.pem"
file_p12="${cn}.keycert.p12"

if [ -f $file_key ] && [ -f $file_req ] && [ -f $file_cer ] && [ -f $file_p12 ];
then
    echo "Nothing to do, certificates already exist"
    exit 0
fi

echo "Generating key.pem"

openssl genrsa -out $file_key $strength

echo "Generating req.pem"

openssl req -new -key $file_key -out $file_req -outform PEM -subj /CN=master.test.openampere.com/O=Server/ -nodes
#-subj "/C=$country/ST=$state/L=$city/O=$org/CN=$cn" -nodes

cd ../ca

echo "Generating cert.pem"

openssl ca -config openssl.cnf -in "../server/${file_req}" -out "../server/${file_cer}" -notext -batch -extensions server_ca_extensions

cd ../server

echo "Generating keycert.p12"

openssl pkcs12 -export -out $file_p12 -in $file_cer -inkey $file_key -passout pass:$password