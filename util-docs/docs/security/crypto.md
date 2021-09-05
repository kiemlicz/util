# Standards
Certificates (keys) are stored in wide range of formats.  
ASN.1 defines the structure of the key/certificate which can later be saved as binary (DER) or 'textual' (PEM)

## [PEM](https://tools.ietf.org/html/rfc1421)
[Base64](http://stackoverflow.com/questions/201479/what-is-base-64-encoding-used-for) translation of the x509 ASN.1 keys placed between well-known delimeters (e.g. `-----BEGIN PRIVATE KEY-----`)

## [DER](https://en.wikipedia.org/wiki/X.690#DER_encoding)
x509 ASN.1 keys

## Formats

### PKCS#1
### PKCS#8

# Certificates
Asymmetric, public key cryptography using trusted institution certifying ownership of public key.

Setting key-pair (with self-signed CA) for server consists of following steps:

1. create private key for CA
2. create self-signed CA cert
3. create private key for server
4. create csr (certificate signing request) for server
5. sign csr using CA

Multiple parameters asked during certificate creation can be specified using config files:
https://www.openssl.org/docs/manmaster/apps/config.html

# References
1. https://tls.mbed.org/kb/cryptography/asn1-key-structures-in-der-and-pem