from castervoice.lib.ctrl.mgr.errors import DontUseBaseClassError


class BaseComboValidator(object):
    """
    Identifies and rejects invalid rules; has access to their
    RuleDetails objects.
    """

    def validate(self, rule, details):
        raise DontUseBaseClassError(self)
