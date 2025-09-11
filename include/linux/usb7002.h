//SPDX-License-Identifier: GPL-2.0-only
//Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.

#ifdef CONFIG_USB7002_HUB
int usb7002_switch_peripheral(void);
int usb7002_switch_host(void);
#else
static inline int usb7002_switch_peripheral(void) {
	return 0;
}
static inline int usb7002_switch_host(void) {
	return 0;
}
#endif
