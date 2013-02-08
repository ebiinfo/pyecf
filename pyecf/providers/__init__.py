from pyecf.error import BinaryNotRegisteredError, PlatformNotSupportedError, ProviderRegistredError

__author__ = 'igor'

import sys

from ctypes import cdll
from inspect import getargspec
from datetime import date

__registred_providers = {}


class ProviderBase(object):
    def __init__(self):
        self.lib = None
        self._so_name = None
        self._dll_name = None

    def registrar_dll(self, name):
        self._dll_name = name

    def registrar_so(self, name):
        self._so_name = name

    def _load_lib(self):
        if sys.platform.startswith('linux'):
            if self._so_name:
                self.lib = cdll.LoadLibrary(self._so_name)
            else:
                raise BinaryNotRegisteredError()
        elif sys.platform.startswith('win'):
            if self._dll_name:
                self.lib = cdll.LoadLibrary(self._dll_name)
            else:
                raise BinaryNotRegisteredError()
        else:
            raise PlatformNotSupportedError()

    def _get_fiscal(self):
        if not self._fiscal.lib:
            self._fiscal.lib = self.get_lib()
        return self._fiscal

    def _set_fiscal(self, component):
        self._fiscal = component

    def get_lib(self):
        if not self.lib:
            self._load_lib()
        return self.lib

    fiscal = property(_get_fiscal, _set_fiscal)


class ManipuladorErro(object):
    _return_codes = {}

    def registrar_codigo_erro(self, code, error):
        def r():
            raise error()

        self._return_codes[code] = r

    def registrar_codigo_ok(self, code):
        def ok():
            pass

        self._return_codes[code] = ok

    def parse_code(self, return_code):
        if return_code == 'ok':
            return
        self._return_codes[return_code]()

    def __call__(self, func):
        def env(*args, **kwargs):
            self.parse_code(func(*args, **kwargs))

        return env


class ParseCodigo(object):
    def __init__(self, func):
        self.parse = func

    def __call__(self,f):
        def env(*args, **kwargs):
            self.parse(f(*args, **kwargs))

        return env


class FuncoesBase(object):
    def __init__(self):
        self.lib = None
        self.parse_codigo = None

#    def __getattr__(self, name):
#        meth = getattr(self,'_%s' % name)
#        def f(*args,**kwargs):
#            self.parse_codigo(meth(*args,**kwargs))
#
#        f.__doc__ = meth.__doc__
#
#        return f


class Formatador(object):
    def __init__(self, *fields):
        self.formato = fields[0] if '%' in fields[0] else self._formato
        self.fields = fields

    def __call__(self, f):
        f_spec = getargspec(f)
        f_args = f_spec.args

        def envelope(*args, **kwargs):
            n_args = list(args)

            if len(args):
                for i in xrange(len(args)):
                    if f_args[i] in self.fields:
                        n_args[i] = self._formata(args[i])
            if len(kwargs):
                for key in kwargs.keys():
                    if key in self.fields:
                        kwargs[key] = self._formata(kwargs[key])
            return f(*n_args, **kwargs)

        return envelope


class formatar_data(Formatador):
    def __init__(self, *fields):
        Formatador.__init__(self, *fields)

    _formato = "%02d/%02d/%s"

    def _formata(self, valor):
        assert type(valor) is date
        return self.formato % valor.timetuple()[:3][::-1]


class formatar_float(Formatador):
    def __init__(self, *fields):
        Formatador.__init__(self, *fields)

    _formato = "%.2f"

    def _formata(self, valor):
        return (self.formato % valor).replace('.', ',')


def register_provider(name, cls):
    if name in __registred_providers.keys():
        raise ProviderRegistredError()
    else:
        __registred_providers[name] = cls


def get_provider(name):
    return __registred_providers[name]()


import bematech
import epson