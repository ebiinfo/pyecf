__author__ = 'igor'

import providers

class Driver(object):
    def __init__(self, provider):
        self._provider = provider
        self.fiscal = provider._get_fiscal()


def get_driver(provider):
    if type(provider) is str:
        return Driver(providers.get_provider(provider))
    else:
        return Driver(provider())