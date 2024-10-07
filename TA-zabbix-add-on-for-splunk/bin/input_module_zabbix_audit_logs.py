
# encoding = utf-8
import datetime
import requests
import json
import traceback

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

# Get audit logs based on time checkpoint
def get_audit_logs(ZABBIX_API_URL,auth_token, start_time):
    payload = {
        "jsonrpc": "2.0",
        "method": "auditlog.get",
        "params": {
            "time_from": start_time,
            "output": "extend",  # You can modify this based on what data you need
            "limit": 1000,
            "sortfield": "clock",
            "sortorder": "ASC"
        },
        "auth": auth_token,
        "id": 2
    }

    headers = {'Content-Type': 'application/json-rpc'}
    response = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
    return response.json()

# Convert datetime to Unix timestamp
def datetime_to_unix(dt):
    return int(dt.timestamp())

# Load the checkpoint (the last `clock` value from the previous run)
def load_checkpoint(helper,key):
    checkpoint = helper.get_check_point(key)
    if checkpoint !=None:
        return checkpoint
    # Default to 24 hours back if no checkpoint exists
    return datetime_to_unix(datetime.datetime.now() - datetime.timedelta(days=30))

# Save the last `clock` value as checkpoint
def save_checkpoint(helper,key,last_clock):
    try:
        helper.save_check_point(key, last_clock)
    except Exception as e:
        helper.log_error("Error while saving checkpoint")
        helper.log_error(traceback.format_exc())


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # api_key = definition.parameters.get('api_key', None)
    pass

def collect_events(helper, ew):

    auth_token = helper.get_arg('api_key')
    # get input type
    helper.get_input_type()

    helper.get_input_stanza()
    log_level = helper.get_log_level()
    global_zabbix_server_url_ip = helper.get_global_setting("zabbix_server_url_ip")
    zabbix_web_ui_protocol = helper.get_global_setting("zabbix_web_ui_protocol")
    global_zabbix_server_port = helper.get_global_setting("zabbix_http_port_web_ui_")
    
    ZABBIX_API_URL = str(zabbix_web_ui_protocol).lower() + "://" + global_zabbix_server_url_ip + ":" + global_zabbix_server_port + "/zabbix/api_jsonrpc.php"
    helper.set_log_level(log_level)

    # # To create a splunk event
    # helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    # import random
    # data = str(random.randint(0,100))
    # event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    # ew.write_event(event)

    try:

        key = str(helper.get_input_stanza_names())
        start_time = load_checkpoint(helper,key)
        audit_logs = get_audit_logs(ZABBIX_API_URL,auth_token, start_time)
        
        # Check and print logs
        if 'result' in audit_logs:
            if(len(audit_logs['result'])>0):
                for log in audit_logs['result']:
                    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=json.dumps(log))
                    ew.write_event(event)
                    # print(json.dumps(log, indent=4))  # Print each log entry in a readable format
                last_log = audit_logs['result'][-1]
                last_clock = int(last_log['clock'])
                save_checkpoint(helper,key,last_clock)
                helper.log_info(f"New checkpoint saved: {last_clock}")
            else:
                helper.log_info("No new audit logs found.")
        else:
            helper.log_info(f"Error fetching audit logs: {audit_logs}")
    except Exception as e:
        helper.log_info(f"An error occurred: {e}")
