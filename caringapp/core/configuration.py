import os


def get_setting(setting_name: str) -> str:
    return os.environ[setting_name]


def get_current_stage() -> str:
    return get_setting('STAGE')


def get_service_name() -> str:
    return get_setting('SERVICE_NAME')


def get_region_name() -> str:
    return get_setting('AWS_REGION')
