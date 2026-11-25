# NeverSettle Kernel
## Kernel Details

| Parameter | Value |
| ---------- | ---------- |
| NS version | 5.3 |
| Linux Kernel version | 4.19.325-cip137-st21 |
| BakaSU version | 4.2.0-rc3 |
| BakaSU version code | 35285 |
| SUSFS version | 2.4.0 |

## Kernel Features
(1) Supports 5V-6A Fast Charging 

(2) Supports Boeffla Wakelock blocker

(3) Using power efficient workqueues

(4) Supports Schedhorizon CPU governor

(5) Global timeout for wakelock

(6) Supports Wireguard VPN

(7) Supports BakaSU with SUSFS

(8) Supports WPA3 SAE WiFi authentication

(9) De-OPLUS-ified kernel, removed unwanted OPLUS code additions

## Credits

- [Linux Kernel Organisation](https://kernel.org): For the development of base kernel
- [weishu](https://github.com/tiann): For the development of KernelSU
- [AlexLiuDev233](https://github.com/AlexLiuDev233): For the development of BakaSU
- [simonpunk](https://gitlab.com/simonpunk): For the development of SUSFS4KSU
- [osm0sis](https://github.com/osm0sis): For the development of AnyKernel3

Linux kernel
============

There are several guides for kernel developers and users. These guides can
be rendered in a number of formats, like HTML and PDF. Please read
Documentation/admin-guide/README.rst first.

In order to build the documentation, use ``make htmldocs`` or
``make pdfdocs``.  The formatted documentation can also be read online at:

    https://www.kernel.org/doc/html/latest/

There are various text files in the Documentation/ subdirectory,
several of them using the Restructured Text markup notation.
See Documentation/00-INDEX for a list of what is contained in each file.

Please read the Documentation/process/changes.rst file, as it contains the
requirements for building and running the kernel, and information about
the problems which may result by upgrading your kernel.
