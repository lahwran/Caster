from dragonfly import (Function, Key, BringApp, Text, WaitWindow, IntegerRef, Dictation, Choice, Grammar, MappingRule)
from dragonfly.actions.action_startapp import StartApp

from lib import utilities, settings
from asynch.hmc import h_launch
from lib.element import scanner


def experiment():
    '''this function is for tests'''
    try: 
        h_launch.launch(settings.QTYPE_DIRECTORY, scan_directory, None)
    except Exception:
        utilities.simple_log(False)

def scan_directory(data):
    scanner.scan_directory(data["path"])
    for k in scanner.DATA:
        print k

class DevRule(MappingRule):
    
    mapping = {
    'refresh directory':            Function(utilities.clear_pyc),
    "(show | open) documentation":  BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) + WaitWindow(executable=settings.get_default_browser_executable()) + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),

    "open natlink folder":          BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "experiment":                   Function(experiment),
    }
    extras = [
              Dictation("text"),
              Dictation("textnv"),
              
             ]
    defaults = {
               "text": ""
               }


grammar = None

def load():
    grammar=Grammar('development')
    grammar.add_rule(DevRule())
    grammar.load()

if settings.SETTINGS["miscellaneous"]["dev_commands"]:
    load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None