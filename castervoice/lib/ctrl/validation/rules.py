class BaseRuleValidator(object):

    def is_applicable(self, declared_ccrtype):
        return False

    def _is_valid(self, rule):
        return True

    def _invalid_message(self):
        return "base rule message -- you should not see this"

    def validate(self, rule):
        if not self._is_valid(rule):
            return self._invalid_message()
        else:
            return None
from castervoice.lib.merge.mergerule import MergeRule


class IsMergeRuleValidator(BaseRuleValidator):

    def is_applicable(self, declared_ccrtype):
        return declared_ccrtype is not None

    def _is_valid(self, rule):
        return isinstance(rule, MergeRule)

    def _invalid_message(self):
        return "must be or inherit MergeRule"
from castervoice.lib.const import CCRType


class NotTreeRuleValidator(BaseRuleValidator):

    def is_applicable(self, declared_ccrtype):
        return declared_ccrtype == CCRType.SELFMOD

    def _is_valid(self, rule):
        return not hasattr(rule, "master_node")

    def _invalid_message(self):
        return "must not be or inherit TreeRule"
class CCRRuleValidationDelegator(object):

    def __init__(self, *validator_delegates):
        self._validator_delegates = validator_delegates

    def validate_rule(self, rule, declared_ccrtype):
        invalidations = []
        for delegate in self._validator_delegates:
            if delegate.is_applicable(declared_ccrtype):
                invalidation = delegate.validate(rule)
                if invalidation is not None:
                    invalidations.append(invalidation)
        return None if len(invalidations) == 0 else ", ".join(invalidation)
from castervoice.lib.const import CCRType
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule


class CCRSelfModifyingRuleValidator(BaseRuleValidator):

    def is_applicable(self, declared_ccrtype):
        return declared_ccrtype == CCRType.SELFMOD

    def _is_valid(self, rule):
        return isinstance(rule, BaseSelfModifyingRule)

    def _invalid_message(self):
        return "must inherit BaseSelfModifyingRule"
