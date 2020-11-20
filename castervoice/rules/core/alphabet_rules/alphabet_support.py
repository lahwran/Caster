from dragonfly import Choice

from castervoice.lib.actions import Key, Text


def caster_alphabet():
    return {
        "one": "1",
        "two": "2",
        "three": "3",
        "for": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "zero": "0",
        "arch"    : "a",
        "brov"    : "b",
        "char"    : "c",
        "delta"   : "d",
        "echo"    : "e",
        "foxy"    : "f",
        "goof"    : "g",
        "hotel"   : "h",
        "India"   : "i",
        "julia"   : "j",
        "kilo"    : "k",
        "Lima"    : "l",
        "Mike"    : "m",
        "Novakeen": "n",
        "oscar"   : "o",
        "prime"   : "p",
        "Quebec"  : "q",
        "Romeo"   : "r",
        "Sierra"  : "s",
        "tango"   : "t",
        "uniform" : "u",
        "victor"  : "v",
        "whiskey" : "w",
        "x-ray"   : "x",
        "yankee"  : "y",
        "Zulu"    : "z",
    }


def get_alphabet_choice(spec):
    return Choice(spec, caster_alphabet())


def letters(big, dict1, dict2, letter):
    '''used with alphabet.txt'''
    d1 = str(dict1)
    if d1 != "":
        Text(d1).execute()
    if big:
        Key("shift:down").execute()
    letter.execute()
    if big:
        Key("shift:up").execute()
    d2 = str(dict2)
    if d2 != "":
        Text(d2).execute()


def letters2(big, letter):
    if big:
        Key(letter.capitalize()).execute()
    else:
        Key(letter).execute()

