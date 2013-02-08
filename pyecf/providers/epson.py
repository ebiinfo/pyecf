from ctypes import c_char_p
from pyecf.error import ParametroInvalidoError
from pyecf.providers import FuncoesBase, ProviderBase, register_provider

__author__ = 'igor'

class EpsonFiscal(FuncoesBase):
    def __init__(self):
        FuncoesBase.__init__(self)
        self.aberto = False

    def _abrir_porta(self, porta=1, velocidade=38400):
        if not self.aberto:
            return self.lib.EPSON_Serial_Abrir_Porta(velocidade, porta)
        return "ok"

    def _leitura_x(self):
        self._abrir_porta()
        return self.lib.EPSON_RelatorioFiscal_LeituraX()

    def _abre_cupom(self):
        return self.lib.EPSON_Fiscal_Abrir_Cupom ( "", "", "", "", 1 )

    def _reducao_z(self, data="", hora=""):
        return self.lib.EPSON_RelatorioFiscal_RZ(data, hora, 2, c_char_p(5) )

class EpsonProvider(ProviderBase):
    def __init__(self):
        ProviderBase.__init__(self)

        self.fiscal = EpsonFiscal()

        self.registrar_so('libInterfaceEpson.so.3')

        self.registrar_codigo_ok(0)

register_provider('epson', EpsonProvider)
