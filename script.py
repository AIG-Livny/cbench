import re
import matplotlib
import matplotlib.pyplot as plt
from itertools import cycle
import warnings
import mapyr

def run(rule:mapyr.Rule):
    print('Running... please wait')

    results : dict = {}
    for p in ['bin/bench-O3-flto','bin/bench-O1']:
        data = mapyr.sh(p,output_capture=True)
        regex_data = re.findall(r'^BENCH (s\d+) (\w+) (.*(?= n)) n=(\d+) t=(.*)', data.stdout, re.MULTILINE)

        for struct, by_what, desc, num, time in regex_data:
            num_bytes = int(struct[1:])
            results.setdefault(p, {}).setdefault(num_bytes, {}).setdefault(desc, {})
            results[p][num_bytes][desc][by_what] = float(time)
            case : dict = results[p][num_bytes][desc]
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