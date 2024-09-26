from flask import Flask, render_template, request, redirect

app = Flask(__name__)
caminho_arquivo = 'notas.txt'

class Aluno:
    def __init__(self, nome, notas):
        self.nome = nome
        self.notas = notas
        self.media = self.calcular_media()

    def calcular_media(self):
        return round(sum(self.notas) / len(self.notas), 2)

    def salvar(self):
        with open(caminho_arquivo, 'a') as arquivo:
            arquivo.write(f"{self.nome};{self.notas[0]};{self.notas[1]};{self.notas[2]};{self.media}\n")

def carregar_alunos():
    alunos = []
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                item = linha.strip().split(';')
                if len(item) == 5:  # Nome + 3 notas + média
                    nome = item[0]
                    notas = [float(nota) for nota in item[1:4]]
                    media = float(item[4])
                    aluno = Aluno(nome, notas)
                    aluno.media = media  # Atribui a média já calculada
                    alunos.append(aluno)
    except FileNotFoundError:
        pass
    return alunos

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular_media", methods=['POST'])
def calcular_media():
    nome_aluno = request.form["nome_aluno"]
    primeira_nota = float(request.form["primeira_nota"])
    segunda_nota = float(request.form["segunda_nota"])
    terceira_nota = float(request.form["terceira_nota"])

    notas = [primeira_nota, segunda_nota, terceira_nota]
    novo_aluno = Aluno(nome_aluno, notas)
    novo_aluno.salvar()

    return redirect("/consultar-notas")

@app.route("/consultar-notas")
def consultar_notas():
    alunos = carregar_alunos()
    return render_template("verificar.html", alunos=alunos)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)



