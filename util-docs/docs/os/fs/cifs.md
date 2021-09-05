# Mount
In order to mount [CIFS](https://en.wikipedia.org/wiki/Server_Message_Block) share on linux, following options are possible:

1. mount with explicit password
2. mount with password in plaintext in file with chmod 600
3. use pam_mount:

_/etc/security/pam_mount.conf.xml_
```

<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE pam_mount SYSTEM "pam_mount.conf.xml.dtd">

<pam_mount>
...
 uncomment this:
<luserconf name=".pam_mount.conf.xml" />
...

</pam_mount>
```

and create _~/.pam_mount.conf.xml_ with:
```
<?xml version="1.0" encoding="utf-8" ?>

<pam_mount>

<volume fstype="cifs" server="server_host" user="*" path="%(USER)" mountpoint="/mnt/%(USER)" options="nosuid,nodev" />
...

</pam_mount>
```

this requires that cifs share for given user has same password as unix user
