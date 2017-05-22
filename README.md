# Consulta CNPJ 

API para consulta de situação cadastral de empresas na base do [SEFAZ](https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjreva_solicitacao.asp).

## Objetivo
* Integrar o sistema de Emissão de Comprovante de Inscrição e de Situação Cadastral da receita federal com outros projetos
quando necessário.

* Não utilizar base de terceiros para a realização da consulta.

* Utilização de web crawler para realizar as leituras dos resultados do SEFAZ.

## Instalação
```shell
$ pip install -r requirements.pip
```

## Utilização
A api tem como base a captação e exibição do captcha, gerado pelo sistema de consulta, através do método 
**generate_captcha**. O retorno é a imagem no formato base64, para facilitar na passagem da mesma para um template HTML,
e a código responsável por validar o captcha.

```python
import pycnpj
sefaz_captcha = pycnpj.generate_captcha()
sefaz_captcha.get('captach')
sefaz_captcha.get('validate_captcha')
```

A obtenção dos dados da empresa é realizado com a passagem do **código de validação**, **Captcha resolvido** e o **CNPJ** da empresa
para o método **consult_sefaz**.
Os dados podem ser consultados de forma única, como somente a razão social ou um **dict** com todas as informações

```python
empresa = pycnpj.consult_sefaz(sefaz_captcha.get('validate_captcha'), 'AsCv98', '06.990.590/0002-04')
print(empresa.razao_social)
print(empresa.json())
```

## Exemplos

No diretório **examples** podem ser encontrados códigos para:
* Flask
* Django