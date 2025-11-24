from flask import Flask, render_template, request, redirect, url_for
import json, os, random

app = Flask(__name__)

ARQ_SENHAS = "senhas.json"
ARQ_SORTEIO = "sorteio.json"

# -------------------------------
# SENHAS INICIAIS
# -------------------------------
senhas_iniciais = {
    "Leticia": "Q9m@4Tz!Lf82",
    "Valentim": "Xp#7vR2!kA91",
    "Joao Vitor": "M8&tR1s#Wq55",
    "Benedito": "Zq!73Lm@pV20",
    "Maria Clara": "S4*eQ9v!Hc18",
    "Carlos": "Tt#29Gm@Kf72",
    "Franciele": "Hb!6Qp3@Zx44",
    "Lucas": "Vr#8mQ2!Lp90",
    "Conceição": "B1@nT5#Gs63",
    "Vitoria": "Nc@3Qx!78Lr5",
    "Duda": "F9*tR6!Hq28",
    "Andrea": "Lp@44Vb!6Tp1",
    "Vinicius": "Kq#82Nc@pM71",
    "Luciano": "Gt@8Tq#43Ls2",
    "Isabela": "Mp!72Qr@Fv99",
    "Renan": "I17o&49Gutb7",
    "Celia": "HXcGm878PR",
}

# -------------------------------
# CRIA JSON DE SENHAS SE NÃO EXISTE
# -------------------------------
if not os.path.exists(ARQ_SENHAS):
    data = {}
    for nome, senha in senhas_iniciais.items():
        data[nome] = {
            "senha": senha,
            "primeiro_login": True
        }
    with open(ARQ_SENHAS, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------------
# SORTEIO (SEM REPETIÇÃO)
# -------------------------------
def sortear(participantes):
    while True:
        embaralhados = participantes[:]
        random.shuffle(embaralhados)
        if all(a != b for a, b in zip(participantes, embaralhados)):
            return dict(zip(participantes, embaralhados))

if not os.path.exists(ARQ_SORTEIO):
    nomes = list(senhas_iniciais.keys())
    resultado = sortear(nomes)
    with open(ARQ_SORTEIO, "w") as f:
        json.dump(resultado, f, indent=4)

# -------------------------------
# ROTA LOGIN
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    with open(ARQ_SENHAS, "r") as f:
        dados = json.load(f)

    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]

        if nome not in dados:
            return render_template("login.html", erro="Nome inválido!", participantes=dados.keys())

        if senha != dados[nome]["senha"]:
            return render_template("login.html", erro="Senha incorreta!", participantes=dados.keys())

        # Primeiro login → obrigatório trocar senha
        if dados[nome]["primeiro_login"]:
            return redirect(url_for("trocar_senha", nome=nome))

        # Já logou antes → mostra amigo secreto
        return redirect(url_for("amigo", nome=nome))

    return render_template("login.html", participantes=dados.keys())

# -------------------------------
# ROTA TROCAR SENHA
# -------------------------------
@app.route("/trocar/<nome>", methods=["GET", "POST"])
def trocar_senha(nome):
    with open(ARQ_SENHAS, "r") as f:
        dados = json.load(f)

    if request.method == "POST":
        nova = request.form["nova"]

        dados[nome]["senha"] = nova
        dados[nome]["primeiro_login"] = False

        with open(ARQ_SENHAS, "w") as f:
            json.dump(dados, f, indent=4)

        # NÃO mostra amigo secreto aqui.
        # Volta pro login.
        return redirect(url_for("login"))

    return render_template("trocar.html", nome=nome)

# -------------------------------
# ROTA MOSTRAR AMIGO SECRETO
# -------------------------------
@app.route("/amigo/<nome>")
def amigo(nome):
    with open(ARQ_SORTEIO, "r") as f:
        sorteio = json.load(f)

    return render_template("amigo.html", nome=nome, amigo=sorteio[nome])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
