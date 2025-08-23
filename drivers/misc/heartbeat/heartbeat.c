//SPDX-License-Identifier: GPL-2.0-only
//Copyright (c) 2024-2025 Qualcomm Innovation Center, Inc. All rights reserved.

#include<linux/init.h>
#include<linux/module.h>
#include<linux/kernel.h>
#include<linux/gpio.h>
#include<linux/of_gpio.h>
#include<linux/platform_device.h>
#include<linux/kobject.h>
#include<linux/sysfs.h>
#include<linux/workqueue.h>
#include<linux/mutex.h>
#include<linux/heartbeat.h>

#define QTI_EVENT_TIMEOUT                3
#define HB_BUFFER_SIZE                   1024
#define HB_PROBE_MAX_RETRY_CNT           3
#define HB_DATA_LENGTH                   4
#define HB_SYSSTATE_FAIL                 1
#define TRIGGER_HB_BUF_SIZE              9
#define HB_REG_WITH_QTI_CAN_SUCCESS      0
#define HB_REG_WITH_QTI_CAN_FAIL         1
#define HB_QTI_CAN_DATA_INVALID          1

typedef struct {
	struct kobject *hb_kobj;
	struct kobj_attribute hb_attr;
	struct delayed_work hb_work;
	struct mutex hb_lock;
	void *qti_can_priv_data;
	char *hb_buf;
	bool mcu_present;
	bool trigger_hb_event;
	char *trigger_hb_buf;
	u8 hb_probe_retry_count;
} heartbeat;

static bool enable_hb_logs;
module_param(enable_hb_logs, bool, 0644);
MODULE_PARM_DESC(enable_hb_logs, "Enable heartbeat logs (false=disabled, true=enabled)");
#define hb_log_info(fmt, ...) \
	do { if (enable_hb_logs) pr_err(fmt, ##__VA_ARGS__); } while(0)

uint32_t sysstate_value;
static heartbeat *hb_priv_data;

int send_heartbeat_event(void *, uint32_t, int);

void trigger_heartbeat_event(const char *driver_name, uint32_t state)
{
	int ret;
        pr_debug("%s: driver_name(%s), state(0x%x)", __func__, driver_name, state);
	mutex_lock(&hb_priv_data->hb_lock);
	sysstate_value = state;
	hb_priv_data->trigger_hb_event = true;
	snprintf(hb_priv_data->trigger_hb_buf, TRIGGER_HB_BUF_SIZE,
			"%8x", state);
	hb_log_info("%s: driver_name(%s), trigger_hb_event(%s), sysstate_value(%x)",
			__func__, driver_name, hb_priv_data->trigger_hb_event, sysstate_value);
	if (hb_priv_data->mcu_present) {
		if (!hb_priv_data->qti_can_priv_data) {
			pr_err("%s: qti_can_priv_data is NULL", __func__);
			mutex_unlock(&hb_priv_data->hb_lock);
			return;
		}
		ret = send_heartbeat_event(hb_priv_data->qti_can_priv_data,
				sysstate_value, HB_DATA_LENGTH);
		if (ret) {
			pr_err("%s: heartbeat event spi transaction failed ret(%d)",
					__func__, ret);
		}
	}

	sysfs_notify(hb_priv_data->hb_kobj, NULL, "sysstate_value");
	mutex_unlock(&hb_priv_data->hb_lock);
}

void send_qti_events(struct work_struct *work)
{
	int ret;

	mutex_lock(&hb_priv_data->hb_lock);
	hb_log_info("%s: sysstate_value(%x)",
			__func__, sysstate_value);
	ret = send_heartbeat_event(hb_priv_data->qti_can_priv_data,
			sysstate_value, HB_DATA_LENGTH);
	if (ret) {
		pr_err("%s: heartbeat event spi transaction failed ret(%d)",
				__func__, ret);
	}

	mutex_unlock(&hb_priv_data->hb_lock);
	schedule_delayed_work(&hb_priv_data->hb_work, QTI_EVENT_TIMEOUT*HZ);
}

static ssize_t android_status_show(struct kobject *kobj,
		struct kobj_attribute *attr, char *buf)
{
	if (hb_priv_data->trigger_hb_event) {
		hb_priv_data->trigger_hb_event = false;
		hb_log_info("%s: trigger_hb_event(%s)",
				__func__, hb_priv_data->trigger_hb_event);
		return snprintf(buf, HB_BUFFER_SIZE, "%s",
				hb_priv_data->trigger_hb_buf);
	} else {
		hb_log_info("%s: hb_buf(%s)",
				__func__, hb_priv_data->hb_buf);
		return snprintf(buf, HB_BUFFER_SIZE, "%s",
				hb_priv_data->hb_buf);
	}
}

static ssize_t android_status_store(struct kobject *kobj,
		struct kobj_attribute *attr, const char *buf, size_t count)
{
	int ret;
	if (count >= HB_BUFFER_SIZE) {
		return -EINVAL;
	}

	strlcpy(hb_priv_data->hb_buf, buf, count+1);
	hb_log_info("%s: hb_buf(%s), count(%d)",
			__func__, hb_priv_data->hb_buf, count);
	mutex_lock(&hb_priv_data->hb_lock);
	sscanf(buf, "%8x", &sysstate_value);
	hb_log_info("%s: sysstate_value(%x)",
			__func__, sysstate_value);
	if (hb_priv_data->mcu_present) {
		ret = send_heartbeat_event(hb_priv_data->qti_can_priv_data,
				sysstate_value, HB_DATA_LENGTH);
		if (ret) {
			pr_err("%s: heartbeat event spi transaction failed ret(%d)",
					__func__, ret);
		}
	}

	mutex_unlock(&hb_priv_data->hb_lock);
	return count;
}

int register_heartbeat(void *qti_can_priv_data)
{
	if (qti_can_priv_data) {
		hb_priv_data->qti_can_priv_data = qti_can_priv_data;
		return HB_REG_WITH_QTI_CAN_SUCCESS;
	}
	return -HB_REG_WITH_QTI_CAN_FAIL;
}
EXPORT_SYMBOL(register_heartbeat);

static int mcu_is_present(struct device *hb_dev)
{
	struct device_node *hb_dev_node;
	int mcu_present = 0;

	if (!hb_dev) {
		pr_err("%s: Heartbeat device is not exist", __func__);
		return -ENODEV;
	}

	hb_dev_node = hb_dev->of_node;
	if (!hb_dev_node) {
		pr_err("%s: Heratbeat node is not exist", __func__);
		return -ENODEV;
	}

	mcu_present = of_property_read_bool(hb_dev_node, "mcu-present");
	return mcu_present;
}

static struct kobj_attribute hb_attr = __ATTR(sysstate_value, 0664, android_status_show, android_status_store);

static int create_hb_sysfs_entry(void)
{
	int ret = 0;

	hb_priv_data->hb_kobj = kobject_create_and_add("qti_heartbeat", NULL);
	if (!hb_priv_data->hb_kobj) {
		pr_err("%s: kobject qti_heartbeat creation failed", __func__);
		return -ENOMEM;
	}

	sysstate_value = 0;
	ret = sysfs_create_file(hb_priv_data->hb_kobj, &hb_attr.attr);
	if (ret) {
		kobject_put(hb_priv_data->hb_kobj);
		pr_err("%s Failed to create /sys/qti_heartbeat/sysstate_value file",
				__func__);
		return -HB_SYSSTATE_FAIL;
	}
	return ret;
}

static int allocate_hb_buffers(void)
{
	int ret = 0;

	hb_priv_data->hb_buf = (char *)kzalloc(HB_BUFFER_SIZE, GFP_KERNEL);
	if (!hb_priv_data->hb_buf) {
		pr_err("%s: Memory allocation failed for hb_buf",
				__func__);
		return -ENOMEM;
	}

	hb_priv_data->trigger_hb_buf = (char *)kzalloc(TRIGGER_HB_BUF_SIZE, GFP_KERNEL);
	if (!hb_priv_data->trigger_hb_buf) {
		kfree(hb_priv_data->hb_buf);
		pr_err("%s: Memory allocation failed for trigger_hb_buf",
				__func__);
		return -ENOMEM;
	}
	return ret;
}

static int qti_heartbeat_probe(struct platform_device *pdev)
{
	int ret = 0;

	if (!hb_priv_data) {
		hb_priv_data = (heartbeat *)kzalloc(sizeof(heartbeat), GFP_KERNEL);
	}

	if (!hb_priv_data) {
		pr_err("%s: Memory allocation failed to heartbeat",
				__func__);
		ret = -ENOMEM;
		goto exit;
	}

	hb_priv_data->mcu_present = mcu_is_present(&pdev->dev);
	if (hb_priv_data->mcu_present) {
		if (!hb_priv_data->qti_can_priv_data) {
			if (hb_priv_data->hb_probe_retry_count < HB_PROBE_MAX_RETRY_CNT) {
				pr_err("%s: trying to hb probe retry count %d",
						__func__, hb_priv_data->hb_probe_retry_count);
				hb_priv_data->hb_probe_retry_count++;
				return -EPROBE_DEFER;
			} else {
				kfree(hb_priv_data);
				pr_err("%s: heartbeat probe failed on invalid \
						qti_can_data", __func__);
				ret = -HB_QTI_CAN_DATA_INVALID;
				goto exit;
			}
		}
	}

	ret = create_hb_sysfs_entry();
	if (ret) {
		kfree(hb_priv_data);
		goto exit;
	}

	ret = allocate_hb_buffers();
	if (ret) {
		sysfs_remove_file(hb_priv_data->hb_kobj, &hb_attr.attr);
		kobject_put(hb_priv_data->hb_kobj);
		kfree(hb_priv_data);
		goto exit;
	}

	mutex_init(&hb_priv_data->hb_lock);
	if (hb_priv_data->mcu_present) {
		INIT_DELAYED_WORK(&hb_priv_data->hb_work, send_qti_events);
		schedule_delayed_work(&hb_priv_data->hb_work, QTI_EVENT_TIMEOUT*HZ);
	}

	pr_info("%s completed", __func__);
exit:
	return ret;
}

static int qti_heartbeat_remove(struct platform_device *pdev) {
	kfree(hb_priv_data->hb_buf);
	kfree(hb_priv_data->trigger_hb_buf);
	sysfs_remove_file(hb_priv_data->hb_kobj, &hb_attr.attr);
	kobject_put(hb_priv_data->hb_kobj);
	if (hb_priv_data->mcu_present) {
		cancel_delayed_work_sync(&hb_priv_data->hb_work);
	}
	kfree(hb_priv_data);
	return 0;
}

static struct of_device_id qti_heartbeat_match_table[] = {
	{ .compatible = "qti,heartbeat" },
	{}
};
MODULE_DEVICE_TABLE(of, qti_heartbeat_match_table);

static struct platform_driver qti_heartbeat_platform_driver = {
	.probe = qti_heartbeat_probe,
	.remove = qti_heartbeat_remove,
	.driver = {
		.name = "qti-heartbeat",
		.owner = THIS_MODULE,
		.of_match_table = of_match_ptr(qti_heartbeat_match_table),
	},
};

module_platform_driver(qti_heartbeat_platform_driver);

MODULE_DESCRIPTION("qti heartbeat driver");
MODULE_LICENSE("GPL v2");
