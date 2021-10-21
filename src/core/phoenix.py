from src.core.git import get_config


def get_template():
    return get_config("phoenix.template-path")
