#!/usr/bin/python3

import copy
import re
import matplotlib
import matplotlib.pyplot as plt
from itertools import cycle
import warnings

def tool_config() -> "mapyr.ToolConfig":
    tc = mapyr.ToolConfig()
    tc.MINIMUM_REQUIRED_VERSION = '0.4.6'
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
    case1.OUT_FILE += ''.join(case1.CFLAGS)
    result.append(case1)

    case2 = copy.deepcopy(default)
    case2.CFLAGS = ["-O1"]
    case2.OUT_FILE += ''.join(case2.CFLAGS)
    result.append(case2)

    return result

def run():
    print('Running... please wait')

    results : dict = {}
    for p in config():
        if mapyr.Project(p).build() == False:
            exit()
        data = mapyr.sh_capture([p.OUT_FILE])
        regex_data = re.findall(r'^BENCH (s\d+) (\w+) (.*(?= n)) n=(\d+) t=(.*)', data, re.MULTILINE)

        for struct, by_what, desc, num, time in regex_data:
            num_bytes = int(struct[1:])
            results.setdefault(p.OUT_FILE, {}).setdefault(num_bytes, {}).setdefault(desc, {})
            results[p.OUT_FILE][num_bytes][desc][by_what] = float(time)
            case : dict = results[p.OUT_FILE][num_bytes][desc]
            if case.get('by_value') and case.get('by_pointer'):
                case['diff'] = case['by_value'] - case['by_pointer']

    cycol = cycle(matplotlib.colors.TABLEAU_COLORS)
    fig, (byval, byptr, relative) = plt.subplots(1, 3, constrained_layout=True)
    for prj_name, prj in results.items():
        cases_points = {}
        for num_bytes, descs in prj.items():
            for desc, values in descs.items():
                if values.get('diff'):
                    cases_points.setdefault(desc,{}).setdefault('xrel',[]).append(num_bytes)
                    cases_points.setdefault(desc,{}).setdefault('yrel',[]).append(values['diff'])
                    cases_points.setdefault(desc,{}).setdefault('xbyval',[]).append(num_bytes)
                    cases_points.setdefault(desc,{}).setdefault('ybyval',[]).append(values['by_value'])
                    cases_points.setdefault(desc,{}).setdefault('xbyptr',[]).append(num_bytes)
                    cases_points.setdefault(desc,{}).setdefault('ybyptr',[]).append(values['by_pointer'])

        for case_name, case in cases_points.items():
            relative.plot(case['xrel'], case['yrel'], color=next(cycol), label=f'{prj_name} {case_name}')
            byval.plot(case['xbyval'], case['ybyval'], color=next(cycol), label=f'{prj_name} {case_name}')
            byptr.plot(case['xbyptr'], case['ybyptr'], color=next(cycol), label=f'{prj_name} {case_name}')

    relative.set_title('Relative')
    relative.set_xscale("log", base=2)
    relative.set_xlabel('struct size')
    relative.set_ylabel('by_val - by_ptr')
    relative.legend(loc="upper left")

    byval.set_title('Absolute by value')
    byval.set_xscale("log", base=2)
    byval.set_xlabel('struct size')
    byval.set_ylabel('cycles')
    byval.legend(loc="upper left")

    byptr.set_title('Absolute by pointer')
    byptr.set_xscale("log", base=2)
    byptr.set_xlabel('struct size')
    byptr.set_ylabel('cycles')
    byptr.legend(loc="upper left")

    warnings.filterwarnings('ignore')
    plt.show()
    pass

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
    mapyr.process(config, tool_config, run)