#!/bin/sh
#
# Simple init script that should handle both
# livecd/livedisk, thinclient and hdd boot
#

PATH=/usr/sbin:/usr/bin:/sbin:/bin
ROOT_LINKS="bin sbin lib boot usr opt"
ROOT_TREES="etc root home var"
TMPFS_DIRS="dev mnt mnt/cdrom mnt/livecd mnt/thin tmp sys proc media"
IMG_DEVICES="hd[a-z] sr[0-9]* scd[a-z]"
LOOP="pardus.img"

NORESUME=0
CDROOT=0
NFSROOT=0
QUIET=0
RAID=0
VIRTIO=0

FS_TYPE=""
ROOT_FLAGS=""
ROOT_LABEL=""
ROOT_UUID=""
ROOT_DEVICE=""
RESUME_DEVICE=""
MNTDIR=""

info() {
    if [ "$QUIET" -eq "0" ]
    then
        echo "[  $(cat /proc/uptime 2>/dev/null | cut -f1 -d' ')0000] initramfs: $1"
    fi
}

fall2sh() {
    echo "--> $*"
    /bin/sh
}


######################
### COOLPLUG stuff ###

# May need to sleep here #
HAS_MASS_STORAGE=0

probe_devices() {
    probe_pci_devices
    probe_usb_devices
    if [ x"$HAS_MASS_STORAGE" == "x1" ]; then
        info "Found USB storage devices."
    fi
    create_device_nodes
}

probe_drm() {
    info "Preparing for KMS"
    for device in /sys/bus/pci/devices/*/boot_vga; do
        [ -f $device ] || continue
        grep -q 1 $device && modprobe -b -q `cat ${device%boot_vga}modalias`
    done
}

probe_pci_devices() {
    info "Probing PCI devices"
    local MODULES=""
    for module in /sys/bus/pci/devices/*/modalias; do
        [ -f $module ] || continue
        MODULES="$MODULES $(cat $module)"
    done
    modprobe -b -q -a $MODULES
}

probe_usb_devices() {
    info "Probing USB devices"
    local MODULES=""
    for module in /sys/bus/usb/devices/*/modalias; do
        [ -f $module ] || continue
        MODULES="$MODULES $(cat $module)"
        grep -qw 08 ${module%modalias}bInterfaceClass && HAS_MASS_STORAGE=1
    done

    modprobe -b -q -a $MODULES
}

create_device_nodes() {
    for block in /sys/block/*; do
        [ -d $block ] || continue
        # block e.g. sda or cciss!c0d0
        NODEPATH="/dev/$(echo $(basename $block) | sed "s,!,/,g")"
        [ ! -d $(dirname $NODEPATH) ] && echo mkdir -p $(dirname $NODEPATH)

        mknod $NODEPATH b $(sed 's/:/ /' $block/dev) &> /dev/null

        # Create partition nodes
        for partitionid in $block/*/partition; do
            [ -f $partitionid ] || continue
            PARTPATH="/dev/$(echo $(basename `dirname $partitionid`) | sed "s,!,/,g")"
            mknod $PARTPATH b $(sed 's/:/ /' "${partitionid%partition}dev") &> /dev/null
        done
    done
}

#####################

probe_raid() {
    info "Probing RAID devices"
    modprobe dm-mod
    modprobe raid0
    modprobe raid1
    modprobe raid10
    modprobe raid456
    /sbin/mdadm --examine --scan > /etc/mdadm.conf
    /sbin/mdadm -As
}

probe_virtio() {
    info "Probing Virtio devices"
    modprobe virtio_pci
    modprobe virtio_balloon
    modprobe virtio_blk
    modprobe virtio_net
}

mount_rootfs() {
    FS_TYPE=`disktype $ROOT_DEVICE | grep KERNELMODULE | awk '{print $2}'`
    if [ -f /lib/modules/*/$FS_TYPE.ko ]
    then
        info "Found module $FS_TYPE, probing it.."
        modprobe $FS_TYPE 1> /dev/null 2>&1
    else
        info "Module $FS_TYPE not found, probably built-in"
    fi
    mount -r -t $FS_TYPE -n ${ROOT_FLAGS} ${ROOT_DEVICE} /newroot
}

resume_from_hibernate() {
    if [ -f "/sys/power/resume" ]
    then
        if [ -f "/bin/resume" ]
        then
            info "Resuming from hibernation"
            # char device needed by static resume binary
            /bin/mknod /dev/snapshot c 10 231
            /bin/resume
        fi
    fi
}

parse_cmdline() {
    for x in `cat /proc/cmdline`; do
        case "${x}" in
            [0123456Ss])
                LEVEL=${x}
            ;;
            mudur=*)
                for m in `echo ${x}|cut -f2 -d=|sed 's/,/ /g'`; do
                    case "${m}" in
                        livecd)
                            CDROOT=1
                        ;;
                        livedisk)
                            CDROOT=1
                            IMG_DEVICES="hd[a-z][0-9]* sd[a-z][0-9]*"
                        ;;
                        raid)
                            RAID=1
                        ;;
                        thin)
                            NFSROOT=1
                        ;;
                        virtio)
                            VIRTIO=1
                        ;;
                    esac
                done
            ;;
            root=*)
                ROOT_DEVICE=`echo ${x}|cut -f2 -d=`
                if [ "${ROOT_DEVICE}" == "LABEL" ]
                then
                    ROOT_LABEL=`echo ${x}|cut -f3 -d=`
                fi
                if [ "${ROOT_DEVICE}" == "UUID" ]
                then
                    ROOT_UUID=`echo ${x}|cut -f3 -d=`
                fi
            ;;
            rootflags=*)
                ROOT_FLAGS="-o ${x#rootflags=}"
            ;;
            resume=*)
                RESUME_DEVICE="${x#resume=}"
            ;;
            init=*)
                INIT="${x#init=}"
            ;;
            quiet)
                QUIET=1
            ;;
            noresume)
                NORESUME=1
            ;;
        esac
    done
}

findcdmount() {
    if [ "$#" -gt "0" ]
    then
        for x in $*
        do
            mount -r ${x} /newroot/mnt/cdrom > /dev/null 2>&1

            if [ "$?" = "0" ]
            then
                # Check for cdroot image
                if [ -e /newroot/mnt/cdrom/${LOOP} ]
                then
                    ROOT_DEVICE="${x}"
                    break
                else
                    umount /newroot/mnt/cdrom
                fi
            fi
        done
    fi
}

manage_tmpfs() {
    mount -t tmpfs tmpfs /newroot

    for d in ${TMPFS_DIRS}
    do
        mkdir -p "/newroot/${d}"
    done

    mv /dev/* /newroot/dev/

    # coolplug may continue making nodes
    mount -o bind /newroot/dev /dev

    # just to make sure, may not be necessary
    [ ! -e /newroot/dev/console ] && mknod /newroot/dev/console c 5 1
}

run_dhcpc() {
    udhcpc -C -i eth0 -s /etc/udhcpc.script
}

mount_nfs() {
    cd /newroot

    # FIXME: busybox mount does not load automatically
    modprobe nfs

    # mount nfs
    if [ -z "/etc/udhcpc.info" ]
    then
        fall2sh "/etc/udhcpc.info not found"
    fi

    . /etc/udhcpc.info

    if [ -z "${ROOTPATH}" ]
    then
        fall2sh "NFS rootpath not found"
    fi

    echo "Mounting NFS from $ROOTPATH"
    mount -o tcp,nolock,ro $ROOTPATH /newroot/mnt/thin

    if [ "$?" != '0' ]
    then
        fall2sh "Could not nfs root"
    fi

    FS_LOCATION='mnt/thin'

    for x in ${ROOT_LINKS}
    do
        ln -s "${FS_LOCATION}/${x}" "${x}"
    done

    chmod 1777 tmp
    (cd /newroot/${FS_LOCATION}; cp -a ${ROOT_TREES} /newroot)

    # Needed for ltspfs mechanism
    echo "$IP    $HOSTNAME" >> /newroot/etc/hosts
}

mount_cdroot() {

    # These are not loaded automatically
    modprobe squashfs

    cd /newroot
    # Loop type squashfs
    mount -t squashfs -o loop,ro /newroot/mnt/cdrom/${LOOP} /newroot/mnt/livecd

    if [ "$?" != "0" ]
    then
        fall2sh "Could not mount root image"
    fi
    FS_LOCATION="mnt/livecd"
    umount /dev

    for x in ${ROOT_LINKS}
    do
        ln -s "${FS_LOCATION}/${x}" "${x}"
    done

    chmod 1777 tmp
    (cd /newroot/${FS_LOCATION}; cp -a ${ROOT_TREES} /newroot)

    # for userspace
    touch /newroot/var/run/pardus/livemedia

    # this is needed for yali
    MNTDIR=`grep \/mnt\/cdrom\  /proc/mounts|sed 's/\/newroot//g'`
    echo "$MNTDIR" >> /newroot/etc/fstab
}

####################
# init starts here #
####################

mount -n -t proc proc /proc > /dev/null 2>&1
mount -n -t sysfs sys /sys > /dev/null 2>&1

# Probe DRM modules for early KMS
probe_drm

# Parse command line arguments
parse_cmdline

info "Starting init on initramfs"

if [ "${ROOT_DEVICE}" == "shellnoprobe" ]
then
    fall2sh "Starting up a shell without probing, as commanded"
elif [ "${ROOT_DEVICE}" == "shell" ]
then
    probe_devices
    fall2sh "Starting up a shell, as commanded"
fi

# Minimizing kernel noise
if [ "$QUIET" -eq "1" ]
then
    echo "1" > /proc/sys/kernel/printk
fi

probe_devices

if [ "${RAID}" -eq "1" ]
then
    probe_raid
fi

if [ "${VIRTIO}" -eq "1" ]
then
    probe_virtio
fi

if [ "${RESUME_DEVICE}" != "" ]
then
    # Write resume device to /sys/power/resume for SATA disks
    /bin/stat -c%t:%T $RESUME_DEVICE > /sys/power/resume

    # If we suspend2disk resume it from here
    resume_from_hibernate
fi

echo 0x0100 > /proc/sys/kernel/real-root-dev

if [ "${CDROOT}" -eq "1" ]
then
    ROOT_DEVICE=""
    manage_tmpfs

    # modprobe filesystems that are not in kernel, for live disks
    for i in nls_cp857 nls_utf8 vfat
    do
        modprobe ${i} 1> /dev/null 2>&1
    done

    for i in `seq 50`
    do
        for t in ${IMG_DEVICES}
        do
            findcdmount "/newroot/dev/$t"
            if [ "${ROOT_DEVICE}" != "" ]
            then
                break
            fi
        done
        if [ "${ROOT_DEVICE}" != "" ]
        then
            break
        else
            probe_devices
            usleep 200000
        fi
    done

    if [ "${ROOT_DEVICE}" == "" ]
    then
        fall2sh "Could not find mount media"
    fi

    mount_cdroot
elif [ "${NFSROOT}" -eq '1' ]
then
    run_dhcpc
    manage_tmpfs
    mount_nfs

    # set hostname for mudur
    hostname $HOSTNAME
else
    # mount real root
    info "Mounting real root"
    for i in `seq 50`
    do
        if [ "${ROOT_LABEL}" != "" ]
        then
            #FIXME: Remove --no-floppy when the problem is fixed in busybox upstream
            ROOT_DEVICE=`findfs LABEL=${ROOT_LABEL} --no-floppy`
        fi

        if [ "${ROOT_UUID}" != "" ]
        then
            #FIXME: Remove --no-floppy when the problem is fixed in busybox upstream
            ROOT_DEVICE=`findfs UUID=${ROOT_UUID} --no-floppy`
        fi

        if [ ! -b "${ROOT_DEVICE}" ]
        then
            probe_devices
            usleep 200000
        else
            break
        fi
    done
    if [ ! -b "${ROOT_DEVICE}" ]
    then
        fall2sh "Could not find boot device"
    else
        mount_rootfs
    fi
fi

info "Preparing to switch to the real root"
umount -n /sys
umount -n /proc

[ "${INIT}" == "" ] && INIT="/sbin/init";

# and we start
exec /bin/switch_root -c /dev/console /newroot ${INIT} ${LEVEL}

