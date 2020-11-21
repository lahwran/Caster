class ComboValidationDelegator(object):

    def __init__(self, *validator_delegates):
        self._validator_delegates = validator_delegates

    def validate(self, rule, details):
        invalidations = []
        for delegate in self._validator_delegates:
            invalidation = delegate.validate(rule, details)
            if invalidation is not None:
                invalidations.append(invalidation)
        return None if len(invalidations) == 0 else ", ".join(invalidations)
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule


class RuleNonEmptyValidator(object):
    """
    Any static rule should have at least one command to start.

    Some selfmod rules don't have any rules the first time they
    are instantiated, but then immediately fill in and "reboot"
    themselves.

    SikuliRule is not a selfmod rule, but it kind of works like
    one, so it is also exempted.
    """

    def validate(self, rule, details):
        invalidations = []
        if len(rule.mapping) == 0 and not self._rule_is_exempt(rule):
            invalidations.append("rules must have at least one command")
        return None if len(invalidations) == 0 else ", ".join(invalidations)

    def _rule_is_exempt(self, rule):
        selfmod = isinstance(rule, BaseSelfModifyingRule)
        sikuli = rule.__class__.__name__ == "SikuliRule"
        return selfmod or sikuli
from dragonfly import MappingRule

from castervoice.lib.const import CCRType
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule


class RuleFamilyValidator(object):
    """
    Non-MappingRules are not handled by Caster.
    MappingRules must not have ccrtypes.
    MergeRules must have ccrtypes.
    SelfModifyingRules can have ccrtypes.
    CCR SelfModifyingRules must use correct type.
    Nothing else is allowed to use SelfModifyingRules CCR type.
    Function Context must not have CCRType `GLOBAL` or `SELFMOD`
    """

    def validate(self, rule, details):
        mapping = isinstance(rule, MappingRule)
        merge = isinstance(rule, MergeRule)
        selfmod = isinstance(rule, BaseSelfModifyingRule)
        has_ccrtype = details.declared_ccrtype is not None
        has_function_context = details.function_context is not None

        invalidations = []

        if not mapping:
            invalidations.append("non-MappingRule rules are not handled")
        elif mapping and not merge and has_ccrtype:
            invalidations.append("MappingRules must not have a ccrtype")
        elif merge and not selfmod:
            if not has_ccrtype:
                invalidations.append("MergeRules must have a ccrtype")
            elif details.declared_ccrtype == CCRType.SELFMOD:
                invalidations.append("non-SelfModifyingRules must not use CCRType.SELFMOD")
        elif selfmod and has_ccrtype and details.declared_ccrtype != CCRType.SELFMOD:
            invalidations.append("CCR SelfModifyingRules must use CCRType.SELFMOD")
        if has_function_context and has_ccrtype:
            if details.declared_ccrtype == CCRType.GLOBAL or details.declared_ccrtype == CCRType.SELFMOD:
                invalidations.append("Function Context cannot be used with `CCRType.GLOBAL` or `CCRType.SELFMOD`")


        return None if len(invalidations) == 0 else ", ".join(invalidations)
from dragonfly import ActionBase
import six
from castervoice.lib.merge.selfmod.tree_rule.tree_node import TreeNode
from castervoice.lib.merge.selfmod.tree_rule.tree_rule import TreeRule


class TreeRuleValidator(object):

    def validate(self, rule, details):
        if not isinstance(rule, TreeRule):
            return None

        return TreeRuleValidator._validate_node(rule._root_node)

    @staticmethod
    def _validate_node(node):
        spec = node.get_spec()
        action = node.get_action()
        children = node.get_children()
        err = str(spec) + ", " + str(action) + ", " + str(children)

        invalidations = []
        if not isinstance(spec, six.string_types):
            invalidations.append("node spec must be string ({})".format(err))
        if not isinstance(action, ActionBase):
            invalidations.append("node base must be ActionBase ({})".format(err))
        for ck in children.keys():
            if not isinstance(children[ck], TreeNode):
                invalidations.append("children must be nodes ({})".format(err))
        return None if len(invalidations) == 0 else ", ".join(invalidations)
