#!/usr/bin/python3

def get_config() -> "ToolConfig":
    tc = ToolConfig()
    tc.MINIMUM_REQUIRED_VERSION = '0.7.0'
    #tc.VERBOSITY = "CRITICAL"
    return tc

def get_rules() -> list['Rule']:

    config1 = c.Config()
    config1.INCLUDE_DIRS = ['c-vector']
    config1.CFLAGS = ["-O3","-flto"]
    config1.LINK_FLAGS = ["-flto"]

    config2 = c.Config()
    config2.INCLUDE_DIRS = ['c-vector']
    config2.CFLAGS = ["-O1"]

    rules = []
    rules.append(Rule('build',['script'], phony=True))
    rules.append(Rule('script',['script.py','bench-O3-flto','bench-O1'],exec=python.run, phony=True))
    rules.append(Rule('script.py'))

    rules.append(Rule('bench-O3-flto',['bin/bench-O3-flto'], downstream_config=config1.__dict__,phony=True))
    rules.append(Rule('bin/bench-O3-flto',['obj/main1.o'],exec=c.link_executable))
    rules.append(Rule('obj/main1.o',['main.c'],exec=c.build_object))

    rules.append(Rule('bench-O1',['bin/bench-O1'], downstream_config=config2.__dict__,phony=True))
    rules.append(Rule('bin/bench-O1',['obj/main2.o'],exec=c.link_executable))
    rules.append(Rule('obj/main2.o',['main.c'],exec=c.build_object))

    rules.append(Rule('main.c'))

    c.add_rules_from_d_file('obj/main.d',rules)
    return rules

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

#-----------FOOTER-----------
try:
    from mapyr import *
except:
    import shutil, subprocess, os
    path = f'{os.path.dirname(__file__)}/mapyr'
    shutil.rmtree(path,ignore_errors=True)
    if subprocess.run(['git','clone','https://github.com/AIG-Livny/mapyr.git',path]).returncode: exit()
    from mapyr import *

if __name__ == "__main__":
    process(get_rules,get_config if 'get_config' in dir() else None)