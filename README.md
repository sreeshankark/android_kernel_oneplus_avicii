# OnePlus Nord (avicii) NeverSettle Kernel Source

<img src="https://raw.githubusercontent.com/sreeshankark/sreeshankark/main/images/ns_logo.png" width=100 height=100 align="left" />  


<img src="https://raw.githubusercontent.com/sreeshankark/sreeshankark/main/images/oneplus_logo.png" align="right"/>

OnePlus Nord (codename:- avicii) is the first upper mid-range non-flagship smartphone from OnePlus Technology Co., Ltd. released in the year 2020.

The phone is available in 2 variants based on region: AC2001 (India) & AC2003 (Europe & Global)

<p align="center">
<img src="https://raw.githubusercontent.com/sreeshankark/sreeshankark/main/images/oneplus_avicii.png" width=500 height=500 />
</p>

| Features | Specification |
| ------------- | ------------- |
| Chipset |  Qualcomm Snapdragon 765G 5G (SM7250-AB) |
| CPU  | Octa-core (1x2.4GHz Single-Core Kryo 475 Prime, 1x2.2GHz Single-Core Kryo 475 Gold & 6x1.8GHz Hexa-Core Kryo 475 Silver)  |
| GPU  | Qualcomm Adreno 620 (625Mhz) |
| RAM  | 6GB/8GB/12GB (LPDDR4X) |
| Shipped OS | Android 10 (Oxygen OS 10) |
| Storage | 64GB/128GB/256GB (UFS2.1) |
| SIM | Hybrid Dual SIM (Nano-SIM, dual stand-by) |
| MicroSD | Not Supported |
| Battery | 4115 mAh (non-removable), Warp Charge 30T fast charging (5V/6A) support |
| Dimensions | 158.3x73.3x8.2 (mm) |
| Weight | 184g |
| Display | 2400x1080, 408ppi, 20:9, 90Hz, Fluid AMOLED |
| Rear Camera (Main) | 48MP (Sony IMX586), 0.8 µm/48M; 1.6 µm (4 in 1)/12M, f/1.75, OIS, EIS, Multi Autofocus (PDAF+CAF) |
| Rear Camera (Ultra wide angle) | 8MP, f/2.25, 119° (FOV) |
| Rear Camera (Depth) | 5MP, f/2.4 |
| Rear Camera (Macro) | 2MP, f/2.4 |
| Flash | Dual LED Flash |
| Front Camera (Main) | 32MP (Sony IMX616), 0.8 µm/32M; 1.6 µm (4 in 1)/8M, f/2.45, EIS, Fixed focus |
| Front Camera (Ultra Wide Angle) | 8MP, f/2.45, 105° (FOV) |
| Fingerprint | Goodix (In-display, optical) |
| Sensors | Accelerometer, Electronic compass, Gyroscope, Ambient light sensor, Proximity sensor, Sensor Core |
| Extras | Bluetooth 5.1 (support aptX & aptX HD & LDAC & AAC), NFC enabled |

### ⚠️ This kernel is not allowed to be included in ROM builds without the [developer's](https://t.me/sksanju0910) approval.

## Kernel Details

| Parameter | Value |
| ---------- | ---------- |
| NS version | 3.3 |
| Linux Kernel version | 4.19.325 |
| KernelSU-Next version | 1.0.9 |
| KernelSU-Next version code | 12799 |
| SUSFS version | 1.5.9 |

## Kernel Features
(1) Supports 5V-6A Fast Charging 

(2) Supports OPlusExtras
- Touchboost
- KCAL
- HBM
- FSync
- Adrenoboost
- Force Fast Charge

(3) Compiled using Clang-LLVM 20.0.0

(4) Supports Boeffla Wakelock blocker

(5) Using power efficient workqueues

(6) Supports Schedhorizon CPU governor

(7) Global timeout for wakelock

(8) Supports Wireguard VPN

(9) Supports KernelSU-Next & SUSFS

(10) Supports WPA3 SAE WiFi authentication

## Credits

- [Linux Kernel Organisation](https://kernel.org): For the development of base kernel
- [weishu](https://github.com/tiann): For the development of KernelSU
- [Rifat Azad](https://github.com/rifsxd): For the development of KernelSU-Next
- [simonpunk](https://gitlab.com/simonpunk): For the development of SUSFS4KSU
- [osm0sis](https://github.com/osm0sis): For the development of AnyKernel3
