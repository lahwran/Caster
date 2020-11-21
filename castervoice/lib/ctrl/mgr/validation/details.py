from castervoice.lib.const import CCRType


class AppCCRDetailsValidator(object):

    '''
    Validates any CCR (APP-type) Details
    '''
    def validate(self, details):
        invalidations = []
        if details.declared_ccrtype == CCRType.APP:
            if details.executable is None:
                invalidations.append("ccr app types must have 'executable'")

        return None if len(invalidations) == 0 else ", ".join(invalidations)


class CCRDetailsValidator(object):
    """
    Validates any CCR Details
    """

    def validate(self, details):
        invalidations = []
        if details.declared_ccrtype is not None:
            if details.name is not None:
                invalidations.append("ccr types must not have 'name'")
            if details.grammar_name is not None:
                invalidations.append("ccr types must not have 'grammar_name'")

        return None if len(invalidations) == 0 else ", ".join(invalidations)
class DetailsValidationDelegator(object):

    def __init__(self, *validator_delegates):
        self._validator_delegates = validator_delegates

    def validate_details(self, details):
        invalidations = []
        for delegate in self._validator_delegates:
            invalidation = delegate.validate(details)
            if invalidation is not None:
                invalidations.append(invalidation)
        return None if len(invalidations) == 0 else ", ".join(invalidations)


class NonCCRDetailsValidator(object):
    """
    Validates any non-CCR Details
    """

    def validate(self, details):
        invalidations = []
        if details.declared_ccrtype is None:
            if details.name is None:
                invalidations.append("non-ccr types must have 'name'")
            if details.get_filepath() is None:
                invalidations.append("non-ccr types must not have a filepath")

        return None if len(invalidations) == 0 else ", ".join(invalidations)
