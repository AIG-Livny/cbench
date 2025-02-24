#!/usr/bin/python3

def get_config() -> 'core.ToolConfig':
    tc = core.ToolConfig()
    tc.MINIMUM_REQUIRED_VERSION = '0.8.0'
    tc.VERBOSITY = "CRITICAL"
    return tc

def get_project(name:str) -> 'core.ProjectBase':

    o3config = c.Config()
    o3config.INCLUDE_DIRS = ['c-vector']
    o3config.CFLAGS = ["-O3","-flto"]
    o3config.LINK_FLAGS = ["-flto"]
    o3config.SOURCES = ['main.c']
    o3config.OBJ_PATH = 'obj/o3'
    o3project = c.Project('o3','bin/bench-O3-flto',o3config)

    o1config = c.Config()
    o1config.INCLUDE_DIRS = ['c-vector']
    o1config.CFLAGS = ["-O1"]
    o1config.SOURCES = ['main.c']
    o1config.OBJ_PATH = 'obj/o1'
    o1project = c.Project('o1','bin/bench-O1',o1config)

    c.add_default_rules(o3project)
    c.add_default_rules(o1project)

    mainpro = core.ProjectBase('main','build',core.ConfigBase())
    script_rule = core.Rule('script.py',mainpro,[o1project.main_rule,o3project.main_rule])

    build_rule = core.Rule('build',mainpro,[script_rule],python.run,phony=True)
    clean_rule = core.Rule('clean',mainpro,[o1project.find_rule('clean'),o3project.find_rule('clean')],phony=True)

    mainpro.rules.append(build_rule)
    mainpro.rules.append(clean_rule)

    return mainpro

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
    core.process(get_project,get_config)