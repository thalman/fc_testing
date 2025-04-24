#!/bin/bash -x

CADIR=`dirname $0`/ca

rm -r -f "$CADIR" >/dev/null 2>&1
mkdir "$CADIR"
pushd "$CADIR"

cat > ca.cnf <<EOF
[ ca ]
default_ca = CA_default

[ CA_default ]
dir              = .
database         = \$dir/index.txt
new_certs_dir    = \$dir/newcerts

certificate      = \$dir/rootCA.crt
serial           = \$dir/serial
private_key      = \$dir/rootCA.key
RANDFILE         = \$dir/rand

default_days     = 3650
default_crl_days = 30
default_md       = sha256

policy           = policy_any
email_in_dn      = no

name_opt         = ca_default
cert_opt         = ca_default
copy_extensions  = copy

[ usr_cert ]
authorityKeyIdentifier = keyid, issuer

[ v3_ca ]
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always,issuer:always
basicConstraints       = CA:true
keyUsage               = critical, digitalSignature, cRLSign, keyCertSign

[ policy_any ]
organizationName       = supplied
organizationalUnitName = supplied
commonName             = supplied
emailAddress           = optional

[ req ]
distinguished_name = req_distinguished_name
prompt             = no

[ req_distinguished_name ]
O  = IdM Federation Example 
OU = IdM Federation Example Test
CN = IdM Federation Example Test CA
EOF

#################

cat > tls.cnf <<EOF
[ req ]
default_bits       = 4096
distinguished_name = req_distinguished_name
req_extensions     = req_ext
prompt             = no

[ req_distinguished_name ]
O = IdM Federation Example
OU = IdM Federation Example Test
CN = \$ENV::hostname

[ req_ext ]
subjectAltName = @alt_names

[ v3_ca ]
extendedKeyUsage = serverAuth, clientAuth, codeSigning, emailProtection
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = \$ENV::hostname
EOF

#################

touch serial index.txt crlnumber index.txt.attr
mkdir newcerts
echo 'unique_subject = no' > index.txt.attr
openssl rand -hex 16 > serial

# Key/Cert pair for RootCA
openssl genrsa -out rootCA.key 4096
openssl req -batch -config ca.cnf \
    -x509 -new -nodes -key rootCA.key -sha256 -days 10000 \
    -set_serial 0 -extensions v3_ca -out rootCA.crt

# Key/Cert pair for Keycloak
openssl genrsa -out keycloak.key 4096
hostname=keycloak openssl req -new -nodes -key keycloak.key \
    -reqexts req_ext -config tls.cnf -out keycloak.csr
hostname=keycloak openssl ca -config ca.cnf -batch -notext -keyfile rootCA.key \
    -extensions v3_ca -extfile tls.cnf \
    -in keycloak.csr -days 3650 -out keycloak.crt

# Key/Cert pair for Web server
openssl genrsa -out web.key 4096
hostname=web openssl req -new -nodes -key web.key \
    -reqexts req_ext -config tls.cnf -out web.csr
hostname=web openssl ca -config ca.cnf -batch -notext -keyfile rootCA.key \
    -extensions v3_ca -extfile tls.cnf \
    -in web.csr -days 3650 -out web.crt


keytool -import \
    -keystore ./truststore.keystore \
    -file ./rootCA.crt \
    -alias federation_example \
    -trustcacerts -storepass Secret123 -noprompt

popd


