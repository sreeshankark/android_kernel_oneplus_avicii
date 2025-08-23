/*
 * Copyright (c) 2025 Qualcomm Innovation Center, Inc. All rights reserved.
 * This header file contains status codes and a generic API prototype that can be called by any driver in case of failure.
 */

#ifndef  HEARTBEAT_H
#define  HEARTBEAT_H

#include <linux/types.h>

#define BOOT_COMPLETED         0x10000000  // Android boot completed
#define STATUS_OK              0x10010000  // Android system is running fine
#define POWER_EVENTS_SHUTDOWN  0x20020000  // Android power events like POWEROFF, RESTART or LPM
#define POWER_EVENTS_REBOOT    0x20020001  // Android Reboot is triggered
#define POWER_EVENTS_S2R       0x20020002  // Android Suspend to RAM (S2R) is triggered
#define LMKD                   0x20030000  // Android LMKD events are triggered
#define LOW_RAM                0x20040000  // System is running on low memory
#define HIGH_CPU_LOAD          0x20050000  // CPU usage is high
#define NW_CONN_FAIL           0x20060000  // Network connection fail
#define FRAMEWORK_FAIL         0x40070000  // Android framework process is killed or crashed or stuck in T / Z / D state
#define KERNEL_PANIC           0x40080000  // Kernel panic occurred
#define DISPLAY_VSYNC_MISS     0x40090000  // Vsync events miss or display frame drops causing UI Freeze and glitch
#define DISPLAY_UNDERRUN       0x400A0000  // Display couldn't keep up with the data, causing a delay or stutter
#define DISPLAY_COMMIT_FAILURE 0x400B0000  // Display fails to update new information

#ifdef CONFIG_QTI_HEARTBEAT
void trigger_heartbeat_event(const char *driver_name, uint32_t state);
#else
void trigger_heartbeat_event(const char *driver_name, uint32_t state) { }
#endif

#endif

