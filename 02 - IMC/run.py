from flask import Flask, render_template, request, redirect

app = Flask(__name__)
caminho_arquivo = 'imc.txt'

class Aluno:
    def __init__(self, nome, peso, altura):
        self.nome = nome
        self.peso = peso
        self.altura = altura
        self.imc = self.calcular_imc()

    def calcular_imc(self):
        return round(self.peso / (self.altura ** 2), 2)

    def classificar_imc(self):
        if self.imc < 18.5:
            return "Abaixo do peso"
        elif 18.5 <= self.imc < 24.9:
            return "Peso normal"
        elif 25 <= self.imc < 29.9:
            return "Sobrepeso"
        elif 30 <= self.imc < 34.9:
            return "Obesidade grau I"
        elif 35 <= self.imc < 39.9:
            return "Obesidade grau II"
        else:
            return "Obesidade grau III ou mórbida"

    def salvar(self):
        with open(caminho_arquivo, 'a') as arquivo:
            arquivo.write(f"{self.nome};{self.peso};{self.altura};{self.imc}\n")

def carregar_alunos():
    alunos = []
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                item = linha.strip().split(';')
                if len(item) == 4:
                    alunos.append(Aluno(item[0], float(item[1]), float(item[2])))
    except FileNotFoundError:
        pass
    return alunos

def salvar_alunos(alunos):
    with open(caminho_arquivo, 'w') as arquivo:
        for aluno in alunos:
            arquivo.write(f"{aluno.nome};{aluno.peso};{aluno.altura};{aluno.imc}\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar_aluno", methods=['POST'])
def cadastrar_aluno():
    nome_aluno = request.form["nome_aluno"]
    peso = float(request.form["peso"])
    altura = float(request.form["altura"])
    
    novo_aluno = Aluno(nome_aluno, peso, altura)
    novo_aluno.salvar()

    return redirect("/consultar-imc")

@app.route("/consultar-imc")
def consultar_imc():
    alunos = carregar_alunos()
    return render_template("consultar-imc.html", alunos=alunos)

@app.route("/deletar_aluno", methods=['POST'])
def deletar_aluno():
    nome_aluno = request.form["nome_aluno"]
    alunos = carregar_alunos()

    alunos = [aluno for aluno in alunos if aluno.nome != nome_aluno]
    salvar_alunos(alunos)

    return redirect("/consultar-imc")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)
