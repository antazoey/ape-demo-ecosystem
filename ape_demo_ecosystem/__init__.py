from ape import plugins

from .ecosystem import DemoEcosystem


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    yield DemoEcosystem
