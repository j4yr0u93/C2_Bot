import os.path
import qtoml as toml

__version__ = 'hazelnut'
CONFIG_PATH = os.path.join('C2_Bot', 'config', 'discon.toml')
MOD_PATH = os.path.join('C2_Bot', 'mods')
mod_list = os.listdir(MOD_PATH)

def load_config(path):
    with open(path, 'r') as f:
        config = toml.load(f)
        return config

discon = load_config(CONFIG_PATH)
