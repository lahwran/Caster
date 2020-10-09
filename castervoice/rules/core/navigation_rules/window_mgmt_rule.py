from dragonfly import MappingRule, Function, Repeat, Choice

from castervoice.lib import utilities
from castervoice.lib import virtual_desktops
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R







def by_name(function, **kwargs):
    def wrapper(desktop):
        return function(desktop, **kwargs)
    return wrapper

class WindowManagementRule(MappingRule):
    mapping = {
        'maximize':
            R(Function(utilities.maximize_window)),
        'minimize':
            R(Function(utilities.minimize_window)),

        # Workspace management
        "show work [spaces]":
            R(Key("w-tab")),
        "(create | new) work [space]":
            R(Key("wc-d")),
        "close all work [spaces]":
            R(Function(virtual_desktops.close_all_workspaces)),
        "next work [space] [<n>]":
            R(Key("wc-right"))*Repeat(extra="n"),
        "(previous | prior) work [space] [<n>]":
            R(Key("wc-left"))*Repeat(extra="n"),

        # "(focus|go) work [space] <n>":
        #     R(Function(virtual_desktops.go_to_desktop_number)),
        "(focus|go) work [space] <desktop>":
            R(Function(by_name(virtual_desktops.go_to_desktop_number))),
        # "send work [space] <n>":
        #     R(Function(virtual_desktops.move_current_window_to_desktop)),
        "send work [space] <desktop>":
            R(Function(by_name(virtual_desktops.move_current_window_to_desktop))),
        # "move work [space] <n>":
        #     R(Function(virtual_desktops.move_current_window_to_desktop, follow=True)),
        "move work [space] <desktop>":
            R(Function(by_name(virtual_desktops.move_current_window_to_desktop, follow=True))),
    }

    extras = [
        IntegerRefST("n", 1, 20, default=1),
        Choice("desktop", virtual_desktops.names_to_indices())
    ]


def get_rule():
    details = RuleDetails(name="window management rule")
    return WindowManagementRule, details
