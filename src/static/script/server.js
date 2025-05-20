const express = require("express");
const SneaksAPI = require("sneaks-api");
const sneaks = new SneaksAPI();
const app = express();
const PORT = 3000;

app.get("/buscar", (req, res) => {
    const { nome } = req.query;
    if (!nome) return res.status(400).json({ erro: "Nome não fornecido" });

    sneaks.getProducts(nome, 10, (err, produtos) => {
        if (err) return res.status(500).json({ erro: "Erro na Sneaks-API" });
        res.json(produtos);
    });
});

app.listen(PORT, () => {
    console.log(`Sneaks-API rodando em http://localhost:${PORT}`);
});