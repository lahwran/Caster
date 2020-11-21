from dragonfly import Dictation, MappingRule

from castervoice.lib.actions import Key

from castervoice.lib.ctrl.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R


class SQLDeveloperRule(MappingRule):

    mapping = {
        "run this query": R(Key("f9")),
        "format code": R(Key("c-f7")),
        "comment line": R(Key("c-slash")),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1}


def get_rule():
    details = RuleDetails(name="sequel developer",
                          executable="sqldeveloper64W",
                          title="SQL Developer")
    return SQLDeveloperRule, details
