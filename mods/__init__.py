import os.path

MOD_PATH = os.path.join('C2_Bot', 'mods')

def get_mod_list(path):
    mod_list_raw = os.listdir(MOD_PATH)
    mod_list = []
    for i in mod_list_raw:
        if (i[-3:] == '.py') & (i[:-3] != '__init__'):
            mod_list.append(i[:-3])
    return mod_list

__all__ = mod_list = get_mod_list(MOD_PATH)
