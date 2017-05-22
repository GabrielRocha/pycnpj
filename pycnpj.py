from settings import URL_SOLICITACAO, URL_VALIDA, CAPTCHA
from crawler import ConsultaCNPJ
import requests
import base64
import re


def _init_session_sefaz():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    session = requests.Session()
    return session.get(url=URL_SOLICITACAO, headers=headers), session


def _get_image_captcha(session):
    request_captcha = session.get(url=CAPTCHA, stream=True)
    if request_captcha.status_code == 200:
        return base64.b64encode(request_captcha.raw.read())


def generate_captcha():
    _request, session = _init_session_sefaz()
    validate_captcha = "#".join(_request.cookies.get_dict().popitem())
    captcha = _get_image_captcha(session)
    return dict(captcha="data:image/png;base64,{}".format(captcha.decode("utf-8")), validate_captcha=validate_captcha)


def consult_sefaz(validate_captcha, captcha, cnpj):
    _, session = _init_session_sefaz()
    session.cookies.set("flag","1")
    name, value = validate_captcha.split("#")
    session.cookies.set(name, value)
    data = {"origem":"comprovante",
            "cnpj": re.sub("(\.|\/|-)", "", cnpj),
            "txtTexto_captcha_serpro_gov_br": captcha,
            "submit1":"Consultar",
            "search_type": "cnpj"}
    request = session.post(url=URL_VALIDA, data=data)
    if request.url.endswith("Cnpjreva_Comprovante.asp"):
        return ConsultaCNPJ(request.text)
