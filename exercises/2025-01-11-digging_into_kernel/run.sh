qemu-system-x86_64 \
	-kernel bzImage \
	-initrd rootfs.cpio \
	-append "console=ttyS0 root=/dev/ram rdinit=/sbin/init quiet kalsr" \
	-cpu kvm64,+smep,+smap \
	-monitor null \
	--nographic \
    -s
