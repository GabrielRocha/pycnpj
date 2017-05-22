# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import re


class ConsultaCNPJ:
    def __init__(self, html):
        self._soup = BeautifulSoup(html, "html.parser")
        self._soup.find("table").extract()
        table_principal = self._soup.find("form").find_next("table")
        self._dados_empresa = table_principal.findChild("tr").findChild("td").\
            findAll("table")

    @property
    def razao_social(self):
        razao_social = self._dados_empresa[2].findAll("font", limit=2)
        return (razao_social[0].get_text().strip(),
                razao_social[1].get_text().strip())

    @property
    def nome_fantasia(self):
        nome_fantasia = self._dados_empresa[3].findAll("font", limit=2)
        return (nome_fantasia[0].get_text().strip(),
                nome_fantasia[1].get_text().strip())

    @property
    def logadouro(self):
        logadouro = self._dados_empresa[7].findAll("font", limit=6)[0:2]
        return (logadouro[0].get_text().strip(),
                logadouro[1].get_text().strip())

    @property
    def _bs_empresa(self):
        return self._dados_empresa[7].findAll("font", limit=6)

    @property
    def numero(self):
        numero = self._bs_empresa[2:4]
        return numero[0].get_text().strip(), numero[1].get_text().strip()

    @property
    def complemento(self):
        complemento = self._bs_empresa[4:6]
        return (complemento[0].get_text().strip(),
                complemento[1].get_text().strip())

    @property
    def _bs_endereco_aux(self):
        return self._dados_empresa[8].findAll("font", limit=8)

    @property
    def cep(self):
        cep = self._bs_endereco_aux[0:2]
        return cep[0].get_text().strip(), cep[1].get_text().strip()

    @property
    def bairro(self):
        bairro = self._bs_endereco_aux[2:4]
        return bairro[0].get_text().strip(), bairro[1].get_text().strip()

    @property
    def municipio(self):
        municipio = self._bs_endereco_aux[4:6]
        return municipio[0].get_text().strip(), municipio[1].get_text().strip()

    @property
    def uf(self):
        uf = self._bs_endereco_aux[6:8]
        return uf[0].get_text().strip(), uf[1].get_text().strip()

    def json(self):
        return {info: getattr(self, info) for info in dir(self)
                if not re.match("^(_|json)", info)}
