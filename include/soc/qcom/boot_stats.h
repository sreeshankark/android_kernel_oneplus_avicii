/* SPDX-License-Identifier: GPL-2.0-only */
/*
 * Copyright (c) 2013-2018, The Linux Foundation. All rights reserved.
 */
/*
 * Copyright (c) 2023, Qualcomm Innovation Center, Inc. All rights reserved.
 */

#ifndef __QCOM_BOOT_STATS_H__
#define __QCOM_BOOT_STATS_H__

#ifdef CONFIG_MSM_BOOT_TIME_MARKER
void place_marker(const char *name);
void destroy_marker(const char *name);
unsigned long long msm_timer_get_sclk_ticks(void);
static inline int boot_marker_enabled(void) { return 1; }
#else
static inline int init_bootkpi(void) { return 0; }
static inline void exit_bootkpi(void) { };
static inline void place_marker(char *name) { };
static inline void destroy_marker(const char *name) { };
static inline int boot_marker_enabled(void) { return 0; }
static inline unsigned long long msm_timer_get_sclk_ticks(void) { return -EINVAL; }
#endif
#endif /* __QCOM_BOOT_STATS_H__ */
#if 0
#ifdef CONFIG_MSM_BOOT_STATS

#define TIMER_KHZ 32768
extern struct boot_stats __iomem *boot_stats;

struct boot_stats {
	uint32_t bootloader_start;
	uint32_t bootloader_end;
	uint32_t bootloader_display;
	uint32_t bootloader_load_kernel;
	uint32_t load_kernel_start;
	uint32_t load_kernel_end;
#ifdef CONFIG_MSM_BOOT_TIME_MARKER
	uint32_t bootloader_early_domain_start;
	uint32_t bootloader_checksum;
#endif
};

int boot_stats_init(void);
int boot_stats_exit(void);
unsigned long long int msm_timer_get_sclk_ticks(void);
phys_addr_t msm_timer_get_pa(void);
#else
static inline int boot_stats_init(void) { return 0; }
static inline unsigned long long int msm_timer_get_sclk_ticks(void)
{
	return 0;
}
static inline phys_addr_t msm_timer_get_pa(void) { return 0; }
#endif

#ifdef CONFIG_MSM_BOOT_TIME_MARKER
static inline int boot_marker_enabled(void) { return 1; }
void place_marker(const char *name);
void update_marker(const char *name);
void measure_wake_up_time(void);
#else
static inline void place_marker(char *name) { };
static inline void update_marker(const char *name) { };
static inline int boot_marker_enabled(void) { return 0; }
static inline void measure_wake_up_time(void) { };
#endif
#ifdef CONFIG_QTI_RPM_STATS_LOG
uint64_t get_sleep_exit_time(void);
#else
static inline uint64_t get_sleep_exit_time(void) { return 0; }
#endif
#endif
