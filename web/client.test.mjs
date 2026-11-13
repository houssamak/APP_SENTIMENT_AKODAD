import assert from "node:assert/strict";
import test from "node:test";

import { messageErreur, predire, sante } from "./client.js";

const ok = (body, status = 200) => ({
  ok: status >= 200 && status < 300,
  status,
  json: async () => body,
});

test("reconnaît le code stable d'entrée invalide", () => {
  assert.match(messageErreur({ erreur: { code: "ENTREE_INVALIDE" } }, 422), /Texte refusé/);
});

test("reconnaît une clé absente ou invalide", () => {
  assert.match(messageErreur({ erreur: { code: "NON_AUTHENTIFIE" } }, 401), /Clé d'API/);
});

test("reconnaît un accès refusé", () => {
  assert.match(messageErreur({ erreur: { code: "ACCES_REFUSE" } }, 403), /administrateur/);
});

test("reconnaît un modèle indisponible", () => {
  assert.match(messageErreur({ erreur: { code: "MODELE_INDISPONIBLE" } }, 503), /indisponible/);
});

test("fournit un message de repli pour un corps inattendu", () => {
  assert.equal(messageErreur({}, 500), "Erreur de l'API (500).");
});

test("appelle la route santé versionnée", async () => {
  const result = await sante("http://localhost:8000/", "cle-client", async (url) => {
    assert.equal(url, "http://localhost:8000/v1/health");
    return ok({ status: "OK", model: "tfidf-logreg" });
  });
  assert.equal(result.status, "OK");
});

test("envoie la clé client à la santé", async () => {
  await sante("http://localhost:8000", " cle ", async (_url, options) => {
    assert.equal(options.headers["X-API-Key"], "cle");
    return ok({ status: "OK" });
  });
});

test("appelle la route de prédiction avec la clé et le texte", async () => {
  const result = await predire("http://localhost:8000", "cle", "Très bien", async (url, options) => {
    assert.equal(url, "http://localhost:8000/v1/predict");
    assert.equal(options.method, "POST");
    assert.equal(options.headers["X-API-Key"], "cle");
    assert.equal(JSON.parse(options.body).text, "Très bien");
    return ok({ label: "POSITIVE", score: 0.8, text: "Très bien" });
  });
  assert.equal(result.label, "POSITIVE");
});

test("renvoie l'abstention sans la transformer en panne", async () => {
  const result = await predire("http://localhost:8000", "cle", "inconnu", async () =>
    ok({ label: "INDETERMINE", score: 0.51, text: "inconnu" }));
  assert.equal(result.label, "INDETERMINE");
});

test("traduit une entrée invalide en message lisible", async () => {
  await assert.rejects(
    predire("http://localhost:8000", "cle", " ", async () =>
      ok({ erreur: { code: "ENTREE_INVALIDE" } }, 422)),
    /Texte refusé/,
  );
});

test("traduit l'absence de clé en message lisible", async () => {
  await assert.rejects(
    sante("http://localhost:8000", "", async () =>
      ok({ erreur: { code: "NON_AUTHENTIFIE" } }, 401)),
    /Clé d'API/,
  );
});

test("ne révèle pas le détail d'une erreur interne", async () => {
  await assert.rejects(
    predire("http://localhost:8000", "cle", "texte", async () =>
      ok({ erreur: { code: "ERREUR_INTERNE", message: "trace secrète" } }, 500)),
    (error) => error.message === "Erreur de l'API (500).",
  );
});
