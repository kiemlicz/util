/##### BEGIN DECRYPTED PGP MESSAGE/ {
    f=1
    indent=""
    while(gsub(/^[ \t]/, "", $0)) {indent = indent " "}
}
f {
    sub("^" indent, "", $0)
    buf = buf $0 ORS
    if ( /##### END DECRYPTED PGP MESSAGE/ ) {
        #printf "%s-----BEGIN PGP MESSAGE-----\n", indent
        cmd = "echo \"" buf "\" | gpg --armor --batch --trust-model always --encrypt -r " keyname "  2>/dev/null | sed 's/^/" indent "/'"
        system(cmd)
        #printf "%s-----END PGP MESSAGE-----", indent
        f=0
        buf=""
        cmd=""
        indent=""
    }
}
!f && ! /##### END DECRYPTED PGP MESSAGE/ { print $0 }
