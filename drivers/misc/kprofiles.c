// SPDX-License-Identifier: GPL-2.0
/*
 * Copyright (C) 2021 Dakkshesh <dakkshesh5@gmail.com>.
 */

#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/kprofiles.h>

unsigned int mode = 0;
module_param(mode, uint, 0664);

#include <linux/delay.h>
#ifdef CONFIG_AUTO_KPROFILES_MSM_DRM
#include <linux/msm_drm_notify.h>
#elif defined(CONFIG_AUTO_KPROFILES_FB)
#include <linux/fb.h>
#endif

static bool screen_on = true;
static unsigned int mode = 0;
static unsigned int set_mode;
module_param(mode, uint, 0664);

void kprofiles_set_mode_rollback(unsigned int level, unsigned int duration_ms)
{
	if (!level || !duration_ms)
		return;
	set_mode = mode;
	mode = level;
	msleep(duration_ms);
	mode = set_mode;
}

void kprofiles_set_mode(unsigned int level)
{
	if (!level)
		return;
	mode = level;
}

#if defined(CONFIG_AUTO_KPROFILES_MSM_DRM) || defined(CONFIG_AUTO_KPROFILES_FB)
static int common_notifier_callback(struct notifier_block *self,
				unsigned long event, void *data)
{
#ifdef CONFIG_AUTO_KPROFILES_MSM_DRM
	struct msm_drm_notifier *evdata = data;
	int *blank;

unsigned int active_mode(void) {
	if (mode == 1) {
		return 1;
	}

	if (mode == 2) {
		return 2;
	}

	if (mode == 3) {
		return 3;
	}

	else {
		pr_info("Invalid value passed, falling back to level 0\n");
		return 0;
	}
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Dakkshesh");
MODULE_DESCRIPTION("KernelSpace Profiles");
MODULE_VERSION("1.0.0"); 
