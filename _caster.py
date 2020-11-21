#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''
import six

if six.PY2:
    import logging
    logging.basicConfig()

from castervoice.lib import settings # requires DependencyMan to be initialized
settings.initialize()


from castervoice.lib.ctrl.configure_engine import EngineConfigEarly, EngineConfigLate
EngineConfigEarly() # requires settings/dependencies

_NEXUS = None

from castervoice.lib import control

if control.nexus() is None: # Initialize Caster State
    from castervoice.lib.ctrl.loading.content_loader import ContentLoader
    from castervoice.lib.ctrl.loading.content_request_generator import ContentRequestGenerator
    _crg = ContentRequestGenerator()
    _content_loader = ContentLoader(_crg)
    control.init_nexus(_content_loader)
    EngineConfigLate() # Requires grammars to be loaded and nexus

print("\n*- Starting " + settings.SOFTWARE_NAME + " -*")
