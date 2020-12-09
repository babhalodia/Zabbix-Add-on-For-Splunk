
# encoding = utf-8
from pyzabbix import ZabbixMetric, ZabbixSender, ZabbixResponse
def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets the setup parameters and prints them to the log
    zabbix_server_url_ip = helper.get_global_setting("zabbix_server_url_ip")
    helper.log_info("zabbix_server_url_ip={}".format(zabbix_server_url_ip))
    zabbix_server_port = helper.get_global_setting("zabbix_server_port")
    helper.log_info("zabbix_server_port={}".format(zabbix_server_port))

    # The following example gets the alert action parameters and prints them to the log
    zabbix_host = helper.get_param("zabbix_host")
    helper.log_info("zabbix_host={}".format(zabbix_host))

    zabbix_port = helper.get_param("zabbix_port")
    helper.log_info("zabbix_port={}".format(zabbix_port))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """

    helper.log_info("Alert action splunk_to_zabbix started.")

    zabbix_server_url_ip = helper.get_global_setting("zabbix_server_url_ip")
    helper.log_debug("zabbix_server_url_ip={}".format(zabbix_server_url_ip))
    zabbix_server_port = helper.get_global_setting("zabbix_server_port")
    helper.log_debug("zabbix_server_port={}".format(zabbix_server_port))

    # The following example gets the alert action parameters and prints them to the log
    zabbix_host = helper.get_param("zabbix_host")
    helper.log_debug("zabbix_host={}".format(zabbix_host))

    zabbix_port = helper.get_param("zabbix_port")
    helper.log_debug("zabbix_port={}".format(zabbix_port))

    final_zabbix_host = zabbix_server_url_ip
    final_zabbix_port = zabbix_server_port

    if zabbix_host is not None and zabbix_host != "":
        final_zabbix_host = zabbix_host
        
    if zabbix_port is not None and zabbix_port != "":
        final_zabbix_port = zabbix_port

    
    metrics = []
    
    events = helper.get_events()
    for event in events:
        if event.get("zabbix_key")!= None:
            #helper.log_info("event={}".format(event))
            for key in event.keys():
                if key != "zabbix_key" and not key.startswith("__mv_") and key != "rid" and key != "time":
                    if event.get("time") is not None:
                        m = ZabbixMetric(event.get('zabbix_key'), key, event.get(key), int(event.get("time")))
                    else:
                        m = ZabbixMetric(event.get('zabbix_key'), key, event.get(key))
                    metrics.append(m)
        else:
            helper.log_info("\"{}\" is not containing zabbix_key value".format(event))
    helper.log_debug(metrics)    
    zbx = ZabbixSender(final_zabbix_host, int(final_zabbix_port))
    helper.log_debug(zbx)
    zabbix_response = zbx.send(metrics)
    helper.log_info("Zabbix Response " + str(zabbix_response))

    # TODO: Implement your alert action logic here
    return 0

