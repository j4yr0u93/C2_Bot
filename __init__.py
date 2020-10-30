import os.path
import qtoml as toml

__version__ = 'hazelnut'
CONFIG_PATH = os.path.join('config', 'discon.toml')

def load_config(path):
    with open(path, 'r') as f:
        config = toml.load(f)
        return config

discon = load_config(CONFIG_PATH)
