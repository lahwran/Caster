from dragonfly import Dictation, Repeat, MappingRule
from castervoice.lib.const import CCRType

from castervoice.lib.actions import Text, Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.merge.mergerule import MergeRule

# Directional Movement

RIGHT = "(right|ross)"
LEFT = "(left|lease)"
UP = "(up|sauce)"
DOWN = "(down|dunce)"
FORWARD = "(%s|next|forward)" % RIGHT
BACK = "(%s|back|prev|prior|previous)" % LEFT

# Miscellaneous
method = "method"
methods = "methods"
extract = "extract"

# Delay Timer
DELAY = "60"

class JetbrainsRule(MergeRule):
    pronunciation = "jet brains"

    mapping = {
        "quick fix": R(Key("a-enter")),
        "distraction free mode": R(Key("as-d")),
        #"(duplicate|duple) %s" % DOWN: R(Key("c-d")),
        "find action": R(Key("cs-a/%s" % DELAY)),
        "smart autocomplete": R(Key("cs-space/%s" % DELAY)),
        "autocomplete": R(Key("c-space/%s" % DELAY)),
        ##"format [code]": R(Key("ca-l")),
        ##"show doc": R(Key("c-q")),
        #"find class": R(Key("c-n")),
        #"build": R(Key("c-f9")),
        "jetbrains run": R(Key("s-f10")),
        "jetbrains stop": R(Key("c-f2")),
        "%s tab [<n>]" % (FORWARD,): R(Key("a-right/%s" % DELAY)) * Repeat(extra="n"),
        "%s tab [<n>]" % (BACK,): R(Key("a-left/%s" % DELAY)) * Repeat(extra="n"),
        "comment [line]": R(Key("c-slash")),
        "uncomment [line]": R(Key("cs-slash")),
        ##"select ex" : R(Key("c-w")),
        ## "select ex down" : R(Key("cs-w")),
        "find file": R(Key("escape, shift, shift/%s" % DELAY)),
        "find": R(Key("c-f/%s" % DELAY)),
        ## "find %s [match] [<n>]" % FORWARD: R(Key("enter")) * Repeat(extra="n"),
        ## "find %s [match] [<n>]" % BACK: R(Key("s-enter")) * Repeat(extra="n"),
        "jetbrains replace": R(Key("c-r/%s" % DELAY)),
        "find all": R(Key("cs-f/%s" % DELAY)),
        ## "replace [in] (all|files)": R(Key("cs-r")),
        "go <n>": R(Text("%(n)sG")),
        ## "implement (%s|%s)" % (method, methods): R(Key("c-i")),
        ## "override %s" % method: R(Key("c-o")),
        ## "run config": R(Key("as-f10")),
        "jetbrains find (usage|usages)": R(Key("a-f7")),
        #"[go to] (source|declaration)": R(Key("c-b")),
        #"(skraken|smart kraken)": R(Key("cs-space")),
        "go %s [<n>]" % FORWARD: R(Key("ca-right")) * Repeat(extra="n"),
        "go %s [<n>]" % BACK: R(Key("ca-left")) * Repeat(extra="n"),
        #"%s %s [<n>]" % (method, FORWARD): R(Key("a-down")) * Repeat(extra="n"),
        #"%s %s [<n>]" % (method, BACK): R(Key("a-up")) * Repeat(extra="n"),
        "go [to] (%s error|error %s)" % (FORWARD, RIGHT): R(Key("f2")) * Repeat(extra="n"),
        "go [to] (%s error|error %s)" % (BACK, LEFT): R(Key("s-f2")) * Repeat(extra="n"),
        #"[organize|optimize] imports": R(Key("ca-o")) * Repeat(extra="n"),
        #"[move] line %s [<n>]" % UP: R(Key("as-up")) * Repeat(extra="n"),
        #"[move] line %s [<n>]" % DOWN: R(Key("as-down")) * Repeat(extra="n"),
        ##"expand [selection] [<n>]": R(Key("c-w")) * Repeat(extra="n"),
        ##"shrink [selection] [<n>]": R(Key("cs-w")) * Repeat(extra="n"),
        #"auto indent": R(Key("ca-i")),
        ## "close tab [<n>]|tab close [<n>]": R(Key("c-f4/%s" % DELAY)) * Repeat(extra="n"),
        ## "run": R(Key("s-f10")),
        ## "debug": R(Key("s-f9")),
        "redo [<n>]": R(Key("cs-z")) * Repeat(extra="n"),
        "jetbrains settings": R(Key("ca-s/%s" % DELAY) + Key("c-f/%s" % DELAY)),

        ## only works if you disable tabs.
        "close (pane|tab) [<n>]|pane close [<n>]": R(Key("c-f4/%s" % DELAY)) * Repeat(extra="n"),
        "unsplit": R(Key("ca-w,u")),
        "go [to] implementation": R(Key("ca-b")),
        "go [to] (usages|definition|declaration)": R(Key("c-b")),

        ## refactoring
        #"refactor": R(Key("cas-t")),
        "refactor rename": R(Key("s-f6")),
        "refactor inline": R(Key("ca-n")),
        "refactor extract": R(Key("ca-m")),
        "refactor %s [variable|var]" % extract: R(Key("ca-v")),
        "refactor %s field" % extract: R(Key("ca-f")),
        "refactor %s constant" % extract: R(Key("ca-c")),
        "refactor %s (param|parameter)" % extract: R(Key("ca-p")),

        ## window navigation
        "focus editor": R(Key("c-tab/%s,c-tab/%s" % (DELAY, DELAY))),
        "(toggle|toll) project": R(Key("a-1")),
        "(toggle|toll) find": R(Key("a-3")),
        "(toggle|toll) run": R(Key("a-4")),
        "(toggle|toll) terminal": R(Key("a-f12/%s" % DELAY)),
        "(toggle|toll) commit": R(Key("a-0/%s" % DELAY)),
        "(toggle|toll) structure": R(Key("a-7/%s" % DELAY)),
        "(toggle|toll) services": R(Key("a-8/%s" % DELAY)),
        "(toggle|toll) get": R(Key("a-9/%s" % DELAY)),
        "spark": R(Key("cs-v/%s" % DELAY)),

        ## must be bound manually below this point
        #"(kill|delete) %s" % FORWARD: R(Key("a-d,0")),
        "(toggle|toll) tool window [bars]": R(Key("sa-t/%s" % DELAY)),
        "(toggle|toll) database": R(Key("ca-d/%s" % DELAY)),
        "split vertical": R(Text(":vs") + Key("enter")),
        "split horizontal": R(Text(":sp") + Key("enter")),
        "pane %s [<n>]" % UP: R(Key("escape") + Key("c-w,k")) * Repeat(extra="n"),
        "pane %s [<n>]" % DOWN: R(Key("escape") + Key("c-w,j")) * Repeat(extra="n"),
        "(pane next|next pane) [<n>]": R(Key("escape") + Key("c-w,w")) * Repeat(extra="n"),
        "(pane %s|%s pane) [<n>]" % (RIGHT, RIGHT): R(Key("escape") + Key("c-w,l")) * Repeat(extra="n"),
        "(pane %s|%s pane) [<n>]" % (LEFT, LEFT): R(Key("escape") + Key("c-w,h")) * Repeat(extra="n"),
        "file rename | rename file": R(Key("cas-r")),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 10000),
    ]

    defaults = {"n": 1, "mim": ""}


def get_rule():
    details = RuleDetails(
                          executable=["idea", "idea64", "studio64", "pycharm", "rider64", "clion64"],
                          ccrtype=CCRType.APP)
    return JetbrainsRule, details
