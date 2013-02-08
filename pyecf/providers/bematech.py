from pyecf.error import ParametroInvalidoError
from pyecf.providers import formatar_data, formatar_float, ManipuladorErro
from pyecf.providers import ProviderBase, register_provider, FuncoesBase

from ctypes import c_char_p

__author__ = 'igor'


class ManipuladorBematech(ManipuladorErro):
    def __init__(self):
        self.registrar_codigo_ok(1)

        self.registrar_codigo_erro(-2, ParametroInvalidoError)


bema_erro = ManipuladorBematech()


class BematechFiscal(FuncoesBase):
    def __init__(self):
        FuncoesBase.__init__(self)

    @bema_erro
    def leitura_x(self):
        return self.lib.Bematech_FI_LeituraX()

    @bema_erro
    def reducao_z(self, data="", hora=""):
        return self.lib.Bematech_FI_ReducaoZ(c_char_p(data), c_char_p(hora))

    @bema_erro
    def abre_cupom(self, cpf=""):
        return self.lib.Bematech_FI_AbreCupom(cpf)

    @bema_erro
    def vende_item(self, codigo, descricao, aliquota, tipo_quantidadede, quantidade, casas_decimais, valor, tipo_desconto='%', valor_desconto='0000'):
        return self.lib.Bematech_FI_VendeItem(codigo, descricao, aliquota, tipo_quantidadede, quantidade, casas_decimais, valor, tipo_desconto, valor_desconto)

    @bema_erro
    def fecha_cupom(self, formaPagamento, valor):
        return self.lib.Bematech_FI_FechaCupomResumido("Dinheiro", "O cliente e bitolado")
#        return self.lib.Bematech_FI_FechaCupom(c_char_p("Dinheiro"), c_char_p("A"), c_char_p("$"), c_char_p("0000"), c_char_p("35,00"), c_char_p(""))

    @bema_erro
    def cancela_cupom(self):
        return self.lib.Bematech_FI_CancelaCupom()

    @bema_erro
    @formatar_float('valor')
    def sangria(self, valor):
        return self.lib.Bematech_FI_Sangria(valor)

    @bema_erro
    @formatar_float('valor')
    def suprimento(self, valor, forma):
        """
        @param valor o valor a ser depositado no suprimento
        @param forma a forma de pagamento a ser utilizada
        """
        return self.lib.Bematech_FI_Suprimento(valor, forma)

    @bema_erro
    @formatar_data('inicio', 'fim')
    def le_memoria(self, inicio, fim):
        return self.lib.Bematech_FI_LeituraMemoriaFiscalData(inicio, fim)


class BematechProvider(ProviderBase):
    def __init__(self):
        ProviderBase.__init__(self)

        self.fiscal = BematechFiscal()

        self.registrar_so('libbemafiscal.so')
        self.registrar_dll('bemafi32.dll')

register_provider('bematech', BematechProvider)