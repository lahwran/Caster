from castervoice.lib.ctrl.mgr.errors import DontUseBaseClassError


class ActivationRuleGenerator(object):
    def construct_activation_rule(self):
        """
        Returns a rule which has activation commands.
        """
        raise DontUseBaseClassError(self)
