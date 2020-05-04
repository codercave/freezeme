import yaml
from pathlib import Path
from uuid import uuid4

BUCKET_NAME = 'bucket_name'
FILE_VERSION = 'file_version'
REGION = 'region'
CURRENT_FILE_VERSION = '1.0'

default_region = 'eu-central-1'

_settings = {}


def load_settings(path: Path, region: str = default_region):
    global _settings
    
    if _settings == {}:
        if path.exists():
            content = path.read_text()
            _settings = yaml.safe_load(content)
        elif path.parent.exists():
            default_settings = _get_default_settings(path.parent)
            default_settings[REGION] = region
            yml = yaml.dump(default_settings)
            path.write_text(yml)
            _settings = default_settings
        else:
            raise ValueError('invalid path to .freezeme settings file')
    
    return _settings


def _get_default_settings(path: Path):
    default_settings = {FILE_VERSION: CURRENT_FILE_VERSION}
    id = uuid4()
    bucket_name = f'frzm-{path.name[0: 22]}-{id}'.replace(' ', '-')

    default_settings[BUCKET_NAME] = bucket_name
    default_settings[REGION] = default_region

    return default_settings
