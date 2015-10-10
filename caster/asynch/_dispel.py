import winsound

from dragonfly import (Function, Text, Grammar, BringApp, WaitWindow, Key,
                       IntegerRef, Dictation, Mimic, MappingRule)

from caster.lib import settings, utilities
from caster.lib import control
from caster.lib.dfplus.state.short import R
from caster.lib.dfplus.additions import IntegerRefST

class Dispel:  # this needs an entry in the settings file, needs to retain information when Dragon is reset
    def __init__(self):
        self.minute = 60
        self.hour = 3600
        #
        self.settings = utilities.load_json_file(settings.SETTINGS["paths"]["DISPEL_JSON_PATH"])
        self.PERIOD = 25  # number of minutes
        self.DELAY_AMOUNT = 5
        self.remaining = 0
        self.active = False
        self.load()  # load saved settings from last run
        if self.active:
            self.resume()
        
        
    def start(self):
        self.reset()
        Dispel.send_message("T: " + str(self.remaining) + " m")
        control.nexus().timer.add_callback(self.tick, self.minute)
    def resume(self):
        Dispel.send_message("T: " + str(self.remaining) + " m")
        control.nexus().timer.add_callback(self.tick, self.minute)
    def stop(self):
        self.active = False
        self.save_settings()
        Dispel.send_message("Dispel: Terminate")
        control.nexus().timer.remove_callback(self.tick)
    
    def save_settings(self):
        self.settings["remaining"] = self.remaining
        self.settings["active"] = self.active
        utilities.save_json_file(self.settings, settings.SETTINGS["paths"]["DISPEL_JSON_PATH"])
    def load(self):
        if "remaining" in self.settings and "active" in self.settings:
            self.remaining = int(self.settings["remaining"])
            self.active = self.settings["active"]
        else:
            self.remaining = self.PERIOD
            self.active = False
    
    def tick(self):  # one time increment passes
        self.remaining -= 1
        self.save_settings()
        if self.remaining <= 0:
            winsound.PlaySound(settings.SETTINGS["paths"]["ALARM_SOUND_PATH"], winsound.SND_FILENAME)
        Dispel.send_message("T: " + str(self.remaining) + " m")
        
    def delay(self):
        self.remaining += self.DELAY_AMOUNT
        
    def reset(self):
        self.active = True
        self.remaining = self.PERIOD
    
    @staticmethod
    def send_message(msg):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            control.nexus().intermediary.text(msg)
        else:
            utilities.report(msg)

ALARM = Dispel()

class MainRule(MappingRule):
    mapping = {
    "run dispel":                   R(Function(ALARM.start), rdescript="Turn On Ergonomic Alarm"),
    "kill dispel":                  R(Function(ALARM.stop), rdescript="Turn Off Ergonomic Alarm"),
    "resume dispel":                R(Function(ALARM.resume), rdescript="Resume Ergonomic Alarm"),
#
    "delay dispel":                 R(Function(ALARM.delay), rdescript="Delay Ergonomic Alarm"),
    "reset dispel":                 R(Function(ALARM.reset), rdescript="Reset Ergonomic Alarm"),
    }
    extras = [
              IntegerRefST("n", 1, 500),
              IntegerRefST("n2", 1, 500),
              Dictation("text"),
             ]
    defaults = {"n": 1, "n2": 1,
               "text": "",
               }

grammar = Grammar('dispel')
grammar.add_rule(MainRule())
grammar.load() 
