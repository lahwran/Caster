from dragonfly import Repeat, Pause, Function, Choice, MappingRule
from castervoice.lib.const import CCRType

from castervoice.lib.actions import Key, Mouse, Text

from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.ctrl.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve
from castervoice.lib.merge.mergerule import MergeRule

class ChromeRule(MergeRule):
    pronunciation = "chrome"
    mapping = {
        "(new window|win new)":
            R(Key("c-n")),
        "(new incognito window | incognito)":
            R(Key("cs-n")),
        "new tab [repeat <n>]|tab new [repeat <n>]":
            R(Key("c-t") * Repeat(extra="n")),
        "reopen tab [repeat <n>]|tab reopen [repeat <n>]":
            R(Key("cs-t")) * Repeat(extra="n"),
        "close tab [repeat <n>]|tab close [repeat <n>]":
            R(Key("c-w")) * Repeat(extra='n'),
        #"win close|close all tabs":
        #    R(Key("cs-w")),
        "next tab [[repeat] <n>]":
            R(Key("c-tab/70")) * Repeat(extra="n"),
        "previous tab [[repeat] <n>]":
            R(Key("cs-tab/70")) * Repeat(extra="n"),
        #"new tab that":
        #    R(Mouse("middle") + Pause("20") + Key("c-tab")),
        "(navigate|go) back [repeat <n>]":
            R(Key("a-left/80")) * Repeat(extra="n"),
        "(navigate|go) forward [repeat <n>]":
            R(Key("a-right/80")) * Repeat(extra="n"),
        "zoom in [repeat <n>]":
            R(Key("c-plus/20")) * Repeat(extra="n"),
        "zoom out [repeat <n>]":
            R(Key("c-minus/20")) * Repeat(extra="n"),
        "zoom reset":
            R(Key("c-0")),
        "(hard refresh|force refresh)":
            R(Key("c-f5")),
        "find (next|forward) [match] [<n>]":
            R(Key("c-g/20")) * Repeat(extra="n"),
        "find (back|prev|prior|previous) [match] [<n>]":
            R(Key("cs-g/20")) * Repeat(extra="n"),
        # requires an extension in some browsers such as chrome
        #"[toggle] caret browsing":
        #    R(Key("f7")),
        "show chrome history":
            R(Key("c-h")),
        "[focus] address bar":
            R(Key("c-l")),
        "show chrome downloads":
            R(Key("c-j")),
        "add chrome bookmark":
            R(Key("c-d")),
        "bookmark all tabs":
            R(Key("cs-d")),
        "show chrome bookmarks":
            R(Key("cs-o")),
        "[toggle] full screen":
            R(Key("f11")),
        "(show|view) page source":
            R(Key("c-u")),
        "chrome debugger resume":
            R(Key("f8")),
        "chrome debugger step over":
            R(Key("f10")),
        "chrome debugger step into":
            R(Key("f11")),
        "chrome debugger step out":
            R(Key("s-f11")),
        "duplicate tab":
            R(Key("a-d,a-c,c-t/15,c-v/15, enter")),
        #"duplicate window":
        #    R(Key("a-d,a-c,c-n/15,c-v/15, enter")),
        "show chrome (menu | three dots)":
            R(Key("a-f")),
        "show chrome settings":
            R(Key("a-f/5, s")),
        "show chrome task manager":
            R(Key("s-escape")),
        #"(clear history|clear browsing data)":
        #    R(Key("cs-del")),
        "toggle (dev|developer) tools":
            R(Key("cs-i")),
        #"checkout [this] pull request [locally]":
        #    R(Function(github_automation.github_checkoutupdate_pull_request, new=True)),
        #"update [this] pull request [locally]":
        #    R(Function(github_automation.github_checkoutupdate_pull_request, new=False)),
        #"IRC identify":
        #    R(Text("/msg NickServ identify PASSWORD")),
        #"tab <m>|<nth> tab":
        #    R(Key("c-%(m)s%(nth)s")),
        "last tab":
            R(Key("c-9")),
        "second last tab":
            R(Key("c-9, cs-tab")),
        #"switch focus [<n>]":
        #    R(Key("f6/20")) * Repeat(extra="n"),
        "[toggle] bookmark bar":
            R(Key("cs-b")),
        "switch chrome user":
            R(Key("cs-m")),
        "focus notification":
            R(Key("a-n")),
        "allow notification":
            R(Key("as-a")),
        "chrome tab detach":
            R(Key("c-l/20,c-x,c-w/20,c-n/20,c-v/5,enter")),
        "chrome tab cut":
            R(Key("c-l/20,c-x,c-w/20")),
        "chrome tab paste":
            R(Key("c-t/20,c-v/5,enter")),
        "deny notification":
            R(Key("as-a")),
        #"google that":
        #    R(Store(remove_cr=True) + Key("c-t") + Retrieve() + Key("enter")),
        #"wikipedia that":
        #    R(Store(space="+", remove_cr=True) + Key("c-t") + Text(
        #        "https://en.wikipedia.org/w/index.php?search=") + Retrieve() + Key("enter")),
        "show chrome (extensions|plugins)":
            R(Key("a-f/20, l, e/15, enter")),
        "chrome more tools":
            R(Key("a-f/5, l")),
    }
    extras = [
        #Choice("nth", {
        #        "first": "1",
        #        "second": "2",
        #        "third": "3",
        #        "fourth": "4",
        #        "fifth": "5",
        #        "sixth": "6",
        #        "seventh": "7",
        #        "eighth": "8",
        #    }),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 10)
    ]
    defaults = {"n": 1, "m":"", "nth": ""}


def get_rule():
    return ChromeRule, RuleDetails(executable="chrome",
                                   ccrtype=CCRType.APP)
