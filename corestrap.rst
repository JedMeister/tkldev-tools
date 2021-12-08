#/bin/bash -e

cd core
git pull origin master
# or I rename the TurnKey remote to 'turnkey' so I would do:
#git pull turnkey master

make root.build

# remove kernel
cat > rm-kernel <<EOF
OLD_KERNEL=\$(echo /boot/vmlinuz-* | sed 's|/boot/vmlinuz-|linux-image-|')
OLD_KERNEL_VER=\$(echo /boot/vmlinuz-* | sed 's|/boot/vmlinuz-||')
debconf-set-selections << EOF2
\$OLD_KERNEL \$OLD_KERNEL/prerm/removing-running-kernel-\$OLD_KERNEL_VER boolean false
EOF2
DEBIAN_FRONTEND=noninteractive apt-get -y purge linux-image-amd64 \$OLD_KERNEL
EOF
chmod +x rm-kernel
fab-chroot build/root.build/ --script rm-kernel
rm -f rm-kernel

# more cleanup
fab-chroot build/root.build "apt-get clean"
find build/root.build/var/lib/apt/lists -type f \
   \( -name "archive.turnkeylinux.org*" \
   -o -name "deb.debian.org*" \
   -o -name "security.debian.org*" \) \
   -exec rm {} +
fab-chroot build/root.build --script $FAB_PATH/common/conf/turnkey.d/locale
fab-apply-removelist $FAB_PATH/common/removelists/turnkey build/root.build

# copy across corestrap
rsync --delete -Hac build/root.build/ $FAB_PATH/bootstraps/bullseye.corestrap/

# hack to replace default bootstrap
mv $FAB_PATH/bootstraps/bullseye $FAB_PATH/bootstraps/bullseye.bootstrap
ln -s $FAB_PATH/bootstraps/bullseye.corestrap $FAB_PATH/bootstraps/bullseye
