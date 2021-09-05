# Create Box
1. Create QCOW2 backed VM image using libvirt
2. Execute following in the VM
```
useradd vagrant
mkdir ~vagrant/.ssh
chmod 700 ~vagrant/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key" > ~vagrant/.ssh/authorized_keys
chmod 600 ~vagrant/.ssh/authorized_keys
chown -R vagrant.vagrant ~vagrant/.ssh

# Sudoers
sed -i -r 's/(.* requiretty)/#\1/' /etc/sudoers

cat > /etc/sudoers.d/90-vagrant-users <<EOF
# User rules for vagrant
vagrant ALL=(ALL) NOPASSWD:ALL
EOF

apt-get install rsync
```
3. Configure only `eth0` network interface, disable modern predictable network interface names
4. Optionally disable unattended-upgrades
5. Shutdown VM
6. `cp /var/lib/libvirt/images/yourqcowimage box.img`
7. Create the `*.box` using [helper](https://github.com/kiemlicz/util/blob/master/vm/vagrant_functions#L3)
8. If the `*.box` will be uploaded to https://app.vagrantup.com/ generate the sha256 hash using: `openssl sha256 box.img` and provide it in the web interface

# References
1. https://gilmatdub.wordpress.com/2014/08/08/howto-create-a-vagrant-image-box-for-libvirt-kvm/