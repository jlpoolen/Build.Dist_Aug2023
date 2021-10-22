import os
from BaseConfig import Base, UUID

GenPi64Generic = Base | {
    "stage3": os.environ.get("STAGE3", "stage3-arm64.tar.xz"),
    "stage3url": "http://distfiles.gentoo.org/releases/arm64/autobuilds/latest-stage3-arm64.txt",
    "stage3mirror": "http://distfiles.gentoo.org/releases/arm64/autobuilds/",
    "profile": "default/linux/arm64/17.0",
    "initsystem": "openrc",
    "initramfs": "none",
    "service-manager": "rcupdate_add",
    "kernel": [
        "sys-kernel/gentoo-kernel-bin"
    ],
    'portage': {
        "make.conf": dict(
            CFLAGS="-mtune=generic -O2 -pipe",
            CXXFLAGS="${CFLAGS}",
            FCFLAGS="${CFLAGS}",
            FFLAGS="${CFLAGS}",
            USE=["bindist"],
            FEATURES="parallel-fetch parallel-install -userpriv -usersandbox -network-sandbox -pid-sandbox".split(),
            MAKEOPTS=f"-j{len(os.sched_getaffinity(0))} -l{len(os.sched_getaffinity(0))}",
            VIDEO_CARDS="",
            GRUB_PLATFORMS="arm64-efi"
        ),
        "patches/": {},
        "savedconfig/": {
            "sys-kernel/": {
                "linux-firmware": "linux-firmware"
            }
        },
        "env/": {},
        "package.env/": {}
    },
    'groups': [
        dict(name="cron", gid=16),
        dict(name="crontab", gid=248),
        dict(name="plugdev", gid=245),
    ],
    "services": {
            "sshd": "default"
    },
    'image': {
        'name': 'GenPi64Generic.img',
        'size': '8G',
        'format': 'gpt',
        'mount-order': [2, 1, 0],
        'uuid': UUID,
        'partitions': [
            {
                'start': '1MiB',
                'end': '100MiB',
                'format': 'vfat',
                'mount-point': '/boot/efi',
                'mount-options': 'noatime',
                'flags': {
                    'boot': 'on'
                }
            },
            {
              'start': '101MiB',
              'end': '500MiB',
              'format': 'vfat',
              'mount-point': '/boot',
              'mount-options': 'noatime'
            },
            {
                'start': '501MiB',
                'end': '0',
                'format': 'btrfs',
                'mount-point': '/',
                'mount-options': 'noatime,compress=zstd:15,ssd,discard',
                'args': f'--force'
            }
        ]
    }
}