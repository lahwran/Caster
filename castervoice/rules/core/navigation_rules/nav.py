from __future__ import print_function
import subprocess

from dragonfly import Function, Repeat, Dictation, Choice, ContextAction
from castervoice.lib.context import AppContext

from castervoice.lib import navigation, context, textformat, text_utils
from castervoice.rules.core.navigation_rules import navigation_support
from dragonfly.actions.action_mimic import Mimic

from castervoice.lib.actions import Key, Mouse
from castervoice.rules.ccr.standard import SymbolSpecs

try:  # Try first loading from caster user directory
    from alphabet_rules.alphabet_support import caster_alphabet
except ImportError: 
    from castervoice.rules.core.alphabet_rules.alphabet_support import caster_alphabet

try:  # Try  first loading  from caster user directory
    from punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict
except ImportError: 
    from castervoice.rules.core.punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions import AsynchronousAction, ContextSeeker
from castervoice.lib.merge.state.actions2 import UntilCancelled
from castervoice.lib.merge.state.short import S, L, R

_tpd = text_punc_dict()
_dtpd = double_text_punc_dict()


for key, value in _dtpd.items():
    if len(value) == 2:
        _dtpd[key] = value[0] + "~" + value[1]
    elif len(value) == 4:
        _dtpd[key] = value[0:1] + "~" + value[2:3]
    else:
        msg = "Need to deal with nonstandard pair length in double_text_punc_dict: {}"
        raise Exception(msg.format(str(value)))


def rotate_display(angle):
    subprocess.call(["C:\\Users\\Lauren\\Downloads\\display\\display64.exe", "/rotate", angle or "0"])



def change_resolution(offset=1):
    screen = tuple(win32_get())
    available = win32_get_modes()
    if screen not in available:
        new = available[0]
    else:
        index = available.index(screen)

        new = available[max(min(len(available)-1, index+offset), 0)]
    #print("current resolution is: ", screen, new, available)
    win32_set(new[0], new[1])
def resolution_down(nnavi3):
    change_resolution(nnavi3 or 1)
def resolution_up(nnavi3):
    change_resolution(-(nnavi3 or 1))

def win32_get_modes():
    '''
    Get the primary windows display width and height
    '''
    import win32api
    from pywintypes import DEVMODEType, error
    modes = []
    i = 0
    try:
        while True:
            mode = win32api.EnumDisplaySettings(None, i)
            modes.append((
                int(mode.PelsWidth),
                int(mode.PelsHeight),
                int(mode.BitsPerPel),
                ))
            i += 1
    except error:
        pass

    by_size = sorted(modes, key=lambda x: x[0]*x[1])
    max_width, max_height, max_depth = by_size[-1]
    results = []
    seen = set()
    for width, height, depth in by_size:
        ratios = [width/float(max_width), height/float(max_height)]
        distortion = max(ratios)/min(ratios)
        #print("resolution: %s,%s,%s distortion: %s" % (width,height,depth,distortion))
        result = (width,height,distortion)
        if result in seen:
            continue
        seen.add(result)
        results.append(result)
    results = sorted(results, key=lambda x: (int(10*x[2]), -x[0]*x[1]))[:6]
    return [x[:-1] for x in results]




def win32_get():
    '''
    Get the primary windows display width and height
    '''
    import ctypes
    user32 = ctypes.windll.user32
    screensize = (
        user32.GetSystemMetrics(0),
        user32.GetSystemMetrics(1),
        )
    return screensize

def win32_set(width=None, height=None, depth=32):
    '''
    Set the primary windows display to the specified mode
    '''
    # Gave up on ctypes, the struct is really complicated
    #user32.ChangeDisplaySettingsW(None, 0)
    import win32api
    from pywintypes import DEVMODEType
    if width and height:

        if not depth:
            depth = 32

        mode = win32api.EnumDisplaySettings()
        mode.PelsWidth = width
        mode.PelsHeight = height
        mode.BitsPerPel = depth

        win32api.ChangeDisplaySettings(mode, 0)
    else:
        win32api.ChangeDisplaySettings(None, 0)

class Navigation(MergeRule):
    pronunciation = "navigation"

    mapping = {
        "resolution down [<nnavi3>]":
            R(Function(resolution_down), rspec="rotate"),
        "resolution up [<nnavi3>]":
            R(Function(resolution_up), rspec="rotate"),
        "display rotate [<angle>]":
            R(Function(rotate_display), rspec="rotate"),
        # "periodic" repeats whatever comes next at 1-second intervals until "terminate"
        # or "escape" (or your SymbolSpecs.CANCEL) is spoken or 100 tries occur
        # "periodic":
        #     ContextSeeker(forward=[
        #         L(
        #             S(["cancel"], lambda: None),
        #             S(["*"],
        #               lambda fnparams: UntilCancelled(
        #                   Mimic(*filter(lambda s: s != "periodic", fnparams)), 1).execute(
        #                   ),
        #               use_spoken=True))
        #     ]),
        # VoiceCoder-inspired -- these should be done at the IDE level
        # "fill <target>":
        #     R(Key("escape, escape, end"), show=False) +
        #     AsynchronousAction([L(S(["cancel"], Function(context.fill_within_line)))],
        #     time_in_seconds=0.2, repetitions=50 ),
        # "jump in":
        #     AsynchronousAction([L(S(["cancel"], context.nav, ["right", "(~[~{~<"]))],
        #                        time_in_seconds=0.1,
        #                        repetitions=50),
        # "jump out":
        #     AsynchronousAction([L(S(["cancel"], context.nav, ["right", ")~]~}~>"]))],
        #                        time_in_seconds=0.1,
        #                        repetitions=50),
        # "jump back":
        #     AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
        #                        time_in_seconds=0.1,
        #                        repetitions=50),
        # "jump back in":
        #     AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
        #                        finisher=Key("right"),
        #                        time_in_seconds=0.1,
        #                        repetitions=50),

        # keyboard shortcuts
        # 'etave':
        #     R(Key("c-s"), rspec="save"),
        'shock [repeat <nnavi50>]':
            R(Key("enter"), rspec="shock")*Repeat(extra="nnavi50"),
        # "(<mtn_dir> | <mtn_mode> [<mtn_dir>]) [(<nnavi500> | <extreme>)]":
        #     R(Function(text_utils.master_text_v)), # this is now implemented below
        "shift click":
            R(Key("shift:down") + Mouse("left") + Key("shift:up")),
        "stoosh [repeat <nnavi500>]":
            R(Function(navigation.stoosh_keep_clipboard), rspec="stoosh"),
        "cut [repeat <nnavi500>]":
            R(Function(navigation.cut_keep_clipboard), rspec="cut"),
        "spark [repeat <nnavi500>] [(<capitalization> <spacing> | <capitalization> | <spacing>) [(bow|bowel)]]":
            R(Function(navigation.drop_keep_clipboard), rspec="spark"),
        "splat [<splatdir>] [repeat <nnavi10>]":
            R(Key("c-%(splatdir)s"), rspec="splat")*Repeat(extra="nnavi10"),
        "deli [repeat <nnavi50>]":
            R(Key("del/5"), rspec="deli")*Repeat(extra="nnavi50"),
        "clear [repeat <nnavi50>]":
            R(Key("backspace/5:%(nnavi50)d"), rspec="clear"),
        SymbolSpecs.CANCEL:
            R(Key("escape"), rspec="cancel"),
        "shackle":
            R(Key("home/5, s-end"), rspec="shackle"),
        # "(tell | tau) <semi>":
        #     R(Function(navigation.next_line), rspec="tell dock"),
        # "(hark | heart) <semi>":
        #     R(Function(navigation.previous_line), rspec="hark dock"),
        "duple [<nnavi50>]":
            R(Function(navigation.duple_keep_clipboard), rspec="duple"),
        # "Kraken":
        #     R(Key("c-space"), rspec="Kraken"),
        "undo [repeat <nnavi10>]":
            R(Key("c-z"))*Repeat(extra="nnavi10"),
        "redo [repeat <nnavi10>]":
            R(
                ContextAction(default=Key("c-y")*Repeat(extra="nnavi10"),
                              actions=[
                                  (AppContext(executable=["rstudio", "foxitreader"]),
                                   Key("cs-z")*Repeat(extra="nnavi10")),
                              ])),

        # text formatting
        # "set [<big>] format (<capitalization> <spacing> | <capitalization> | <spacing>) [(bow|bowel)]":
        #     R(Function(textformat.set_text_format)),
        # "clear castervoice [<big>] formatting":
        #     R(Function(textformat.clear_text_format)),
        # "peek [<big>] format":
        #     R(Function(textformat.peek_text_format)),
        "(<capitalization> <spacing> | <capitalization> | <spacing>) [(bow|bowel)] <textnv> [brunt]":
            R(Function(textformat.master_format_text)),
        #"[<big>] format <textnv>":
        #    R(Function(textformat.prior_text_format)),
        #"<word_limit> [<big>] format <textnv>":
        #    R(Function(textformat.partial_format_text)),
        # "hug <enclosure>":
        #     R(Function(text_utils.enclose_selected)),
        "dredge [<nnavi10>]":
            R(Key("alt:down, tab/20:%(nnavi10)d, alt:up"),
              rdescript="Core: switch to most recent Windows"),

        # Ccr Mouse Commands
        "kick [<nnavi10>]":
            R(Function(navigation.left_click))*Repeat(extra="nnavi10"),
        "psychic":
            R(Function(navigation.right_click)),
        "(kick double|double kick)":
            R(Function(navigation.left_click)*Repeat(2)),
        "squat":
            R(Function(navigation.left_down)),
        "bench":
            R(Function(navigation.left_up)),

        # keystroke commands
        "<direction> [repeat <nnavi500>]":
            R(Key("%(direction)s")*Repeat(extra='nnavi500'), rdescript="arrow keys"),
        "(lease wally | latch) [repeat <nnavi10>]":
            R(Key("home:%(nnavi10)s")),
        "(ross wally | ratch) [repeat <nnavi10>]":
            R(Key("end:%(nnavi10)s")),
        "sauce wally [repeat <nnavi10>]":
            R(Key("c-home:%(nnavi10)s")),
        "dunce wally [repeat <nnavi10>]":
            R(Key("c-end:%(nnavi10)s")),
        "<modifier> <button_dictionary_500> [repeat <nnavi500>]":
            R(Key("%(modifier)s%(button_dictionary_500)s")*Repeat(extra='nnavi500'),
              rdescript="press modifier keys plus buttons from button_dictionary_500"),
        "<modifier> <button_dictionary_10> [repeat <nnavi10>]":
            R(Key("%(modifier)s%(button_dictionary_10)s")*Repeat(extra='nnavi10'),
              rdescript="press modifier keys plus buttons from button_dictionary_10"),
        "<modifier> <button_dictionary_1>":
              R(Key("%(modifier)s%(button_dictionary_1)s"),
              rdescript="press modifiers plus buttons from button_dictionary_1, non-repeatable"),

        # "key stroke [<modifier>] <combined_button_dictionary>":
        #     R(Text('Key("%(modifier)s%(combined_button_dictionary)s")')),

        # "key stroke [<modifier>] <combined_button_dictionary>":
        #     R(Text('Key("%(modifier)s%(combined_button_dictionary)s")')),
    }
    tell_commands_dict = {"dock": ";", "doc": ";", "sink": "", "com": ",", "deck": ":"}
    tell_commands_dict.update(_tpd)

    # I tried to limit which things get repeated how many times in hopes that it will help prevent the bad grammar error
    # this could definitely be changed. perhaps some of these should be made non-CCR
    button_dictionary_500 = {
        "(tab | tabby)": "tab",
        "(backspace | clear)": "backspace",
        "(delete|deli)": "del",
        "(escape | cancel)": "escape",
        "(enter | shock)": "enter",
        "(left | lease)": "left",
        "(right | ross)": "right",
        "(up | sauce)": "up",
        "(down | dunce)": "down",
        "page (down | dunce)": "pgdown",
        "page (up | sauce)": "pgup",
        "space": "space"
    }
    button_dictionary_10 = {
        "(F{}".format(i) + " | function {})".format(i) : "f{}".format(i)
        for i in range(1, 13)
    }
    button_dictionary_10.update(caster_alphabet())
    button_dictionary_10.update(_tpd)
    longhand_punctuation_names = {
        "minus": "hyphen",
        "hyphen": "hyphen",
        "comma": "comma",
        "deckle": "colon",
        "colon": "colon",
        "slash": "slash",
        "backslash": "backslash"
    }
    button_dictionary_10.update(longhand_punctuation_names)
    button_dictionary_1 = {
        "(home | lease wally | latch)": "home",
        "(end | ross wally | ratch)": "end",
        "insert": "insert",
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    combined_button_dictionary = {}
    for dictionary in [button_dictionary_1, button_dictionary_10, button_dictionary_500]:
        combined_button_dictionary.update(dictionary)

    modifier_choice_object = Choice("modifier", {
            "(control | fly)": "c-", #TODO: make DRY
            "(shift | shin)": "s-",
            "alt": "a-",
            "(control shift | queue)": "cs-",
            "control alt": "ca-",
            "(shift alt | alt shift)": "sa-",
            "(control alt shift | control shift alt)": "csa-",  # control must go first
            "windows": "w-",  # windows should go before alt/shift
            "control windows": "cw-",
            "control windows alt": "cwa-",
            "control windows shift": "cws-",
            "windows shift alt": "wsa-",
            "windows alt shift": "was-",
            "windows shift": "ws-",
            "windows alt": "wa-",
            "control windows alt shift": "cwas-",
            "hit": "",
        })
    extras = [
        IntegerRefST("nnavi10", 1, 11),
        IntegerRefST("nnavi3", 1, 4),
        IntegerRefST("nnavi50", 1, 50),
        IntegerRefST("nnavi500", 1, 500),
        Dictation("textnv"),
        Choice("enclosure", _dtpd),
        Choice("direction", {
            "dunce": "down",
            "sauce": "up",
            "lease": "left",
            "ross": "right",
        }),
        modifier_choice_object,
        Choice("button_dictionary_1", button_dictionary_1),
        Choice("button_dictionary_10", button_dictionary_10),
        Choice("button_dictionary_500", button_dictionary_500),
        Choice("combined_button_dictionary", combined_button_dictionary),

        Choice("capitalization", {
            "capitalize": 1, # THISISATEST
            "camelcaps": 2, # ThisIsATest
            "camelcase": 3, # thisIsATest
            #"caps": 4,
            "laws": 5, # thisisatest
            "dragon say": 6, # this is a test
            "single caps": 7, #This is a test
            "(dragon slip|lowercase)": 8, #this is a test
            "spongebob": 9,  # this is a test
        }),
        Choice(
            "spacing", {
                "(gaps|gapsa)": -1, # this is a test of default, THIS IS A TEST OF YELLING
                "gum": 1, # thisisatest
                "gun": 1,
                "spine": 2, # this-Is-A-Test
                "snake": 3, # This_Is_A_Test
                "pebble": 4,
                "cobble": 9, # this::is::a::test::THIS::IS::A::TEST::this::is::a::test::
                "cobblestone": 8,
                #"incline": 5,
                #"dissent": 6,
                #"descent": 6,
                "dunder": 7,
            }),
        Choice("semi", tell_commands_dict),
        Choice("word_limit", {
            "single": 1,
            "double": 2,
            "triple": 3,
            "Quadra": 4
        }),
        navigation_support.TARGET_CHOICE,
        navigation_support.get_direction_choice("mtn_dir"),
        Choice("mtn_mode", {
            "shin": "s",
            "queue": "cs",
            "fly": "c",
        }),
        Choice("extreme", {
            "Wally": "way",
        })  ,      Choice("angle", {
            "ninety": "90",
            "minus ninety": "270",
            "two [hundred] seventy": "270",
            "zero": "0"
        }),
        Choice("big", {
            "big": True,
        }),
        Choice("splatdir", {
            "lease": "backspace",
            "ross": "delete",
        }),
    ]

    defaults = {
        "nnavi500": 1,
        "nnavi50": 1,
        "nnavi10": 1,
        "nnavi3": 1,
        "textnv": "",
        "capitalization": 0,
        "spacing": 0,
        "mtn_mode": None,
        "mtn_dir": "right",
        "extreme": None,
        "big": False,
        "splatdir": "backspace",
        "modifier": "",
    }


def get_rule():
    return Navigation, RuleDetails(ccrtype=CCRType.GLOBAL)
