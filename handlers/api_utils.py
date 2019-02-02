import os


def set_dynamo_table_name(model):
    service_name = os.environ['SERVICE_NAME']
    stage_name = os.environ['STAGE']
    model.Meta.table_name = \
        '{}-{}-{}'.format(service_name, stage_name, model.Meta.simple_name)
