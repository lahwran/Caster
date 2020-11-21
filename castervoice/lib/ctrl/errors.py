class DontUseBaseClassError(Exception):
    def __init__(self, base_instance):
        super(DontUseBaseClassError, self).__init__(
            "Do not use base class ({}).".format(base_instance.__class__.__name__))
class GuidanceRejectionException(Exception):

    _MSG = "Unit tests should not write files unless they clean them up too."

    def __init__(self):
        super(GuidanceRejectionException, self).__init__(GuidanceRejectionException._MSG)
class ICCEMessage(object):
    COMPANION_TYPE = "MergeRules cannot be companion rules; only MappingRules. {} is invalid."


class InvalidCompanionConfigurationError(Exception):
    def __init__(self, rcn, msg=ICCEMessage.COMPANION_TYPE):
        super(InvalidCompanionConfigurationError, self).__init__(msg.format(rcn))
class ITMessage(object):
    BAD_TYPE = "{} rejected because it no longer descends from its original parent class."
    CLASS_KEY = "{} rejected because its class name changed."


class InvalidTransformationError(Exception):

    def __init__(self, msg, rcn):
        super(InvalidTransformationError, self).__init__(msg.format(rcn))
class NoPronunciationError(Exception):
    """
    This error should NEVER actually be thrown since rules without
    pronunciations should get rejected by loading safety checks.
    """

    def __init__(self, rcn):
        super(NoPronunciationError, self).__init__(
            "Rule has no pronunciation: {}.".format(rcn))
class NotAModuleError(Exception):
    def __init__(self, file_path):
        super(NotAModuleError, self).__init__(file_path + " is not a module.")
class TreeRuleConfigurationError(Exception):
    def __init__(self, msg):
        super(TreeRuleConfigurationError, self).__init__(msg)
