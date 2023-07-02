from base64 import b64encode

import toml


def _read_config_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as config_file:
            config = toml.load(config_file)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the TOML file: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the TOML file: {e}")


def read_config():
    config = _read_config_file("config/config.toml")
    secrets = _read_config_file("config/secrets.toml")
    return config, secrets


config, secrets = read_config()


def _get_nimble_credential_string():
    if secrets:
        nimble_username = secrets["nimble"]["username"]
        nimble_password = secrets["nimble"]["password"]

        nimble_credential_string = b64encode(
            f"{nimble_username}:{nimble_password}".encode("utf-8")
        ).decode("utf-8")
        return nimble_credential_string
