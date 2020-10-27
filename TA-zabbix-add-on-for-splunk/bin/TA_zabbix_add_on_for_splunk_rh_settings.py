
import ta_zabbix_add_on_for_splunk_declare

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    MultipleModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunk_aoblib.rest_migration import ConfigMigrationHandler

util.remove_http_proxy_env_vars()


fields_additional_parameters = [
    field.RestField(
        'zabbix_server_url_ip',
        required=True,
        encrypted=False,
        default='',
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
    ), 
    field.RestField(
        'zabbix_server_port',
        required=True,
        encrypted=False,
        default='10051',
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
    )
]
model_additional_parameters = RestModel(fields_additional_parameters, name='additional_parameters')


endpoint = MultipleModel(
    'ta_zabbix_add_on_for_splunk_settings',
    models=[
        model_additional_parameters
    ],
)


if __name__ == '__main__':
    admin_external.handle(
        endpoint,
        handler=ConfigMigrationHandler,
    )