
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_zabbix_add_on_for_splunk_declare

import os
import sys

from alert_actions_base import ModularAlertBase
import modalert_splunk_to_zabbix_helper

class AlertActionWorkersplunk_to_zabbix(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkersplunk_to_zabbix, self).__init__(ta_name, alert_name)

    def validate_params(self):

        if not self.get_global_setting("zabbix_server_url_ip"):
            self.log_error('zabbix_server_url_ip is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_global_setting("zabbix_server_port"):
            self.log_error('zabbix_server_port is a mandatory setup parameter, but its value is None.')
            return False
        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            if not self.validate_params():
                return 3
            status = modalert_splunk_to_zabbix_helper.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(str(ae)))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e:
                self.log_error(msg.format(str(e)))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkersplunk_to_zabbix("TA-zabbix-add-on-for-splunk", "splunk_to_zabbix").run(sys.argv)
    sys.exit(exitcode)
