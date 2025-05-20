# 👟 Sistema de Recomendação de Tênis

Este é um projeto de recomendação personalizada de tênis utilizando **Flask**, **KNN (Sklearn)** e integração com a **Sneaks-API** para recomendações online.

---

## 🔧 Funcionalidades

- Recomendação baseada em categorias e descrições com KNN.
- Cálculo de chance de acerto baseado na similaridade.
- Integração com a Sneaks-API para buscar modelos reais na internet.
- Interface web com Flask e HTML/CSS.

---

## 🚀 Como executar

### 1. Clone este repositório
- git clone https://github.com/MarcusFonseca7/Anuncio_Perfeito.git
- cd ./Anuncio_Perfeito/src

### 2. Crie e ative o ambiente virtual
   
  a. Windows:
  - python -m venv venv
  - venv\Scripts\activate

  
  b. Linux/Mac:
  - python3 -m venv venv  
  - source venv/bin/activate  

### 3. Instale as dependências Python
- pip install -r requirements.txt

### 4. Instale e rode a Sneaks-API
- (A Sneaks-API precisa do Node.js instalado. Instale por favor!)
- npm install -g sneaks-api
- sneaks-api-server
Isso iniciará um servidor local em http://localhost:3000.

### 5. Inicie o servidor Flask
- Em outra aba do terminal (com o ambiente virtual ainda ativado): "python app.py"

