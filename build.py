#!/usr/bin/python3

import copy

def tool_config() -> "mapyr.ToolConfig":
    tc = mapyr.ToolConfig()
    tc.MINIMUM_REQUIRED_VERSION = '0.4.5'
    tc.VERBOSITY = "CRITICAL"
    return tc

def config() -> list["mapyr.ProjectConfig"]:

    result = []

    default = mapyr.ProjectConfig()
    default.OUT_FILE  = "bin/bench"
    default.COMPILER  = "clang"
    default.GROUPS = ['DEBUG']
    default.SRC_DIRS = ['.']
    default.INCLUDE_DIRS = ['.','c-vector']

    default.VSCODE_CPPTOOLS_CONFIG = True

    case1 = copy.deepcopy(default)
    case1.CFLAGS = ["-O3","-flto"]
    case1.LINK_EXE_FLAGS = ["-flto"]
    result.append(case1)

    return result

#-----------FOOTER-----------
# https://github.com/AIG-Livny/mapyr.git
try:
    import mapyr
except:
    import requests, os
    os.makedirs(f'{os.path.dirname(__file__)}/mapyr',exist_ok=True)
    with open(f'{os.path.dirname(__file__)}/mapyr/__init__.py','+w') as f:
        f.write(requests.get('https://raw.githubusercontent.com/AIG-Livny/mapyr/master/__init__.py').text)
    import mapyr

if __name__ == "__main__":
    mapyr.process(config, tool_config)