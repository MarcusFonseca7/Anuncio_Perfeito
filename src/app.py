import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import requests
import re
from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

TAXA_CAMBIO = 5.65
# Baixa as stopwords
nltk.download('stopwords')
stopwords_pt = stopwords.words('portuguese')

# Carrega os dados e treina o modelo 
df = pd.read_csv("data/dadosNike.csv")
df.columns = df.columns.str.strip().str.lower()

df['texto'] = df['categoria'] + ' ' + df['descricao']

vectorizer = TfidfVectorizer(stop_words=stopwords_pt)
X = vectorizer.fit_transform(df['texto'])

knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(X)

# ------------------ Funções de recomendação ------------------ #

dists_treino, _ = knn.kneighbors(X)
dist_min = dists_treino.min()
dist_max = dists_treino.max()

def calcular_probabilidade(distancia):
    if distancia >= dist_max:
        return 5  # mínimo garantido
    if distancia <= dist_min:
        return 99  # quase certeza

    score = (dist_max - distancia) / (dist_max - dist_min)

    # Aplicando transformação para suavizar e levantar os valores:
    ajustado = np.power(score, 0.25)  # raiz de score
    return round(ajustado * 100, 2)

def recomendar_com_knn(texto_usuario):
    vetor_usuario = vectorizer.transform([texto_usuario])
    distancias, indices = knn.kneighbors(vetor_usuario)
    recomendados = df.iloc[indices[0]].copy()
    recomendados['chance_acerto'] = [calcular_probabilidade(d) for d in distancias[0]]
    return recomendados[['nome', 'categoria', 'descricao', 'chance_acerto']].to_dict(orient='records')

def buscar_com_sneaks_api(nome_tenis):
    try:
        url = "http://localhost:3000/buscar"
        response = requests.get(url, params={'nome': nome_tenis})
        response.raise_for_status()
        dados = response.json()
        if not dados:
            return None

        # Formatando para o HTML
        return [
            {
                'nome': item.get('shoeName'),
                'categoria': item.get('brand'),
                'descricao': item.get('styleID', 'Sem descrição'),
                'imagem': item.get('thumbnail'),
                'preco': round(item.get('retailPrice', 0) * TAXA_CAMBIO, 2)
            }
            for item in dados
        ]
    except Exception as e:
        print("Erro ao acessar a Sneaks-API:", e)
        return None

# ------------------ Rotas Flask ------------------ #

@app.route('/')
def home():
    tenis_lista = df['nome'].tolist()
    return render_template('index.html', tenis_lista=tenis_lista)

@app.route('/recomendacao', methods=['GET', 'POST'])
def recomendacao():
    if request.method == "POST":
        preferencia = request.form['preferencia']
        
        if not re.match(r"^[a-zA-Z0-9'\-+. ]+$", preferencia):
            return render_template('resultado.html', recomendacoes=[], mensagem="Entrada inválida: use apenas letras e números.")
        
        # Tenta Sneaks-API primeiro
        recomendacoes = buscar_com_sneaks_api(preferencia)
        origem = "internet"

        if not recomendacoes:
            recomendacoes = recomendar_com_knn(preferencia)
            origem = "local"

        return render_template('resultado.html', recomendacoes=recomendacoes, origem=origem)

    return render_template('resultado.html')

if __name__ == '__main__':
    app.run(debug=True)