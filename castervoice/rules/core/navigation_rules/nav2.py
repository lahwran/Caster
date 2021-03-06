from dragonfly import Function, Repeat, Dictation, Choice, MappingRule, AppContext, ContextAction

from castervoice.lib.actions import Key, Mouse
from castervoice.lib import navigation, utilities
from castervoice.rules.core.navigation_rules import navigation_support
from castervoice.lib import textformat

try:  # Try first loading from caster user directory
    from alphabet_rules import alphabet_support
except ImportError: 
    from castervoice.rules.core.alphabet_rules import alphabet_support

from castervoice.lib.ctrl.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.actions import AsynchronousAction
from castervoice.lib.merge.state.short import S, L, R


class NavigationNon(MappingRule):

    pronunciation = "navigation companion"

    mapping = {
        "<direction> <time_in_seconds>":
            AsynchronousAction(
                [L(S(["cancel"], Key("%(direction)s"), consume=False))],
                repetitions=1000,
                blocking=False),
        "erase multi clipboard":
            R(Function(navigation.erase_multi_clipboard)),
        "undo [repeat <nnavi10>]":
            R(Key("c-z"))*Repeat(extra="nnavi10"),
        "redo [repeat <nnavi10>]":
            R(
                ContextAction(default=Key("c-y")*Repeat(extra="nnavi10"),
                              actions=[
                                  (AppContext(executable=["rstudio", "foxitreader"]),
                                   Key("cs-z")*Repeat(extra="nnavi10")),
                              ])),
        "shift click":
            R(Key("shift:down") + Mouse("left") + Key("shift:up")),
        "find":
            R(Key("c-f")),
        "find next [<n>]":
            R(Key("f3"))*Repeat(extra="n"),
        "find prior [<n>]":
            R(Key("s-f3"))*Repeat(extra="n"),
        "find everywhere":
            R(Key("cs-f")),
        "replace":
            R(Key("c-h")),
        "F<function_key>":
            R(Key("f%(function_key)s")),
        "[show] context menu":
            R(Key("s-f10")),
        "lean":
            R(Function(navigation.right_down)),
        "hoist":
            R(Function(navigation.right_up)),
        "kick mid":
            R(Function(navigation.middle_click)),
        "shift right click":
            R(Key("shift:down") + Mouse("right") + Key("shift:up")),
        "curse <direction> [<direction2>] [<nnavi500>] [<dokick>]":
            R(Function(navigation.curse)),
        "scree <direction> [<nnavi500>]":
            R(Function(navigation.wheel_scroll)),
        "scree <direction> <time_in_seconds>":
            R(AsynchronousAction(
                [L(S(["cancel"], Function(navigation.wheel_scroll, nnavi500=1)))],
                repetitions=1000,
                blocking=False)),
        "colic":
            R(Key("control:down") + Mouse("left") + Key("control:up")),
        "garb [<nnavi500>]":
            R(Mouse("left") + Mouse("left") + Function(
                navigation.stoosh_keep_clipboard)),
        "drop [<nnavi500>]":
            R(Mouse("left") + Mouse("left") + Function(
                navigation.drop_keep_clipboard,
                capitalization=0,
                spacing=0)),
        "sure stoosh":
            R(Key("c-c")),
        "sure cut":
            R(Key("c-x")),
        "sure spark":
            R(Key("c-v")),
        "(reload|refresh)":
            R(Key("c-r")),
        "maxiwin":
            R(Key("w-up")),
        "move window":
            R(Key("a-space, r, a-space, m")),
        "window left [<n>]":
            R(Key("w-left"))*Repeat(extra="n"),
        "window right [<n>]":
            R(Key("w-right"))*Repeat(extra="n"),
        "window up [<n>]":
            R(Key("w-up"))*Repeat(extra="n"),
        "window down [<n>]":
            R(Key("w-down"))*Repeat(extra="n"),
        "window expand left [<n>]":
            R(Key("wac-left"))*Repeat(extra="n"),
        "window expand right [<n>]":
            R(Key("wac-right"))*Repeat(extra="n"),
        "window expand up [<n>]":
            R(Key("wac-up"))*Repeat(extra="n"),
        "window expand down [<n>]":
            R(Key("wac-down"))*Repeat(extra="n"),
        "take screenshot":
            R(Key("ws-s")),
        "monitor (left | lease) [<n>]":
            R(Key("sw-left"))*Repeat(extra="n"),
        "monitor (right | ross) [<n>]":
            R(Key("sw-right"))*Repeat(extra="n"),
        "(next | prior) window":
            R(Key("ca-tab, enter")),
        "switch (window | windows)":
            R(Key("ca-tab"))*Repeat(extra="n"),
        "next tab [<n>]":
            R(Key("c-pgdown"))*Repeat(extra="n"),
        "prior tab [<n>]":
            R(Key("c-pgup"))*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-w/20"))*Repeat(extra="n"),
        "<capitalization> <textnv>":
            R(Function(textformat.nonccr_format_text)),
    }

    extras = [
        Dictation("text"),
        Dictation("textnv"),
        Dictation("mim"),
        IntegerRefST("function_key", 1, 13),
        IntegerRefST("n", 1, 50),
        IntegerRefST("nnavi500", 1, 5000),
        IntegerRefST("nnavi10", 1, 10),
        Choice("time_in_seconds", {
            "super slow": 5,
            "slow": 2,
            "normal": 0.6,
            "fast": 0.1,
            "superfast": 0.05
        }),
        navigation_support.get_direction_choice("direction"),
        navigation_support.get_direction_choice("direction2"),
        navigation_support.TARGET_CHOICE,
        Choice("dokick", {
            "kick": 1,
            "psychic": 2
        }),
        Choice("capitalization", {
            "say": 6,
            "cop": 7,
            "slip": 8,
        }),
        Choice("wm", {
            "ex": 1,
            "tie": 2
        }),
    ]
    defaults = {
        "n": 1,
        "mim": "",
        "nnavi500": 1,
        "direction2": "",
        "dokick": 0,
        "text": "",
        "wm": 2
    }


def get_rule():
    return NavigationNon, RuleDetails(name="navigation companion")
