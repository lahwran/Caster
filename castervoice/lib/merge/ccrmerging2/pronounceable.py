from castervoice.lib.ctrl.mgr.errors import DontUseBaseClassError


class Pronounceable(object):

    def get_pronunciation(self):
        """
        Child classes should implement this,
        returning string pronunciation.
        """
        raise DontUseBaseClassError(self)
