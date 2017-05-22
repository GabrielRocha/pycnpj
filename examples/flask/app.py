from pycnpj import generate_captcha, consult_sefaz
import flask
import sys
import os
sys.path.append(os.path.realpath('../..'))


app = flask.Flask(__name__, static_url_path="")


@app.route("/", methods=['GET', 'POST'])
def index():
    message = "Consulta CNPJ"
    dados_sefaz = []
    if flask.request.method == "POST":
        try:
            empresa = consult_sefaz(flask.request.form['validate_captcha'],
                                    flask.request.form['captcha'],
                                    flask.request.form['cnpj'])
            dados_sefaz = empresa.json().values()
        except AttributeError:
            message = "CNPJ ou CAPTCHA Inválido"
    return flask.render_template("cnpj.html", **generate_captcha(),
                                 dados_sefaz=dados_sefaz, message=message)


if __name__ == "__main__":
    app.run(debug=True)
