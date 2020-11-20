from dragonfly import MappingRule, Function, RunCommand, Playback

from castervoice.lib import control, utilities
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R



class CasterRule(MappingRule):
    mapping = {
        "clear caster log":
            R(Function(utilities.clear_log)),
        "reboot caster":
            R(Function(utilities.reboot)),

        # ccr de/activation
        "enable (c c r|ccr)":
            R(Function(lambda: control.nexus().set_ccr_active(True))),
        "disable (c c r|ccr)":
            R(Function(lambda: control.nexus().set_ccr_active(False))),
    }


def get_rule():
    return CasterRule, RuleDetails(name="caster rule")
