
# encoding = utf-8
from pyzabbix import ZabbixMetric, ZabbixSender, ZabbixResponse
def process_event(helper, *args, **kwargs):

    helper.log_info("Alert action splunk_to_zabbix started.")

    zabbix_server_url_ip = helper.get_global_setting("zabbix_server_url_ip")
    helper.log_debug("zabbix_server_url_ip={}".format(zabbix_server_url_ip))
    zabbix_server_port = helper.get_global_setting("zabbix_server_trapper_port")
    helper.log_debug("zabbix_server_port={}".format(zabbix_server_port))

    # The following example gets the alert action parameters and prints them to the log
    zabbix_host = helper.get_param("zabbix_host_ip_url_")
    helper.log_debug("zabbix_host={}".format(zabbix_host))

    zabbix_port = helper.get_param("zabbix_port")
    helper.log_debug("zabbix_port={}".format(zabbix_port))

    final_zabbix_host = zabbix_server_url_ip
    final_zabbix_port = zabbix_server_port

    if(zabbix_host != ""):
        final_zabbix_host = zabbix_host
        
    if(zabbix_port != ""):
        final_zabbix_port = zabbix_port

    
    metrics = []
    
    events = helper.get_events()
    for event in events:
        if event.get("zabbix_key")!= None:
            #helper.log_info("event={}".format(event))
            for key in event.keys():
                if key != "zabbix_key" and not key.startswith("__mv_") and key != "rid" and key!="time":
                    if event.get("time")!=None:
                        m = ZabbixMetric(event.get('zabbix_key'), key, event.get(key),int(event.get("time")))
                    else:
                        m = ZabbixMetric(event.get('zabbix_key'), key, event.get(key))
                    metrics.append(m)
        else:
            helper.log_info("\"{}\" is not containing zabbix_key value".format(event))
    helper.log_debug(metrics)    
    zbx = ZabbixSender(final_zabbix_host,int(final_zabbix_port))
    helper.log_debug(zbx)
    zabbix_response = zbx.send(metrics)
    helper.log_info("Zabbix Response "+str(zabbix_response))

    # TODO: Implement your alert action logic here
    return 0