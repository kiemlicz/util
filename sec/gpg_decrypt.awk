/-----BEGIN PGP MESSAGE-----/ {
    f=1
    indent=""
    while(gsub(/^[ \t]/, "", $0)) {indent = indent " "}
}
f {
    gsub(/^[ \t]+/, "", $0)
    buf = buf $0 ORS
    if ( /-----END PGP MESSAGE-----/ ) {
        # once decrypted such marks should be added in plaintext
        #printf "%s##### BEGIN DECRYPTED PGP MESSAGE\n", indent
        cmd = "echo \"" buf "\" | gpg --decrypt 2>/dev/null | sed 's/^/" indent "/'"
        #print cmd | "/bin/bash" # is evaluated after below printf
        system(cmd)
        #printf "%s##### END DECRYPTED PGP MESSAGE", indent
        f=0
        buf=""
        cmd=""
        indent=""
    }
}
!f && ! /-----END PGP MESSAGE-----/ { print $0 }
