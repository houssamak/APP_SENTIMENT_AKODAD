const MESSAGES = {
  ENTREE_INVALIDE: "Texte refusé : vide, composé d'espaces ou trop long.",
  NON_AUTHENTIFIE: "Clé d'API absente ou invalide.",
  ACCES_REFUSE: "Cette opération nécessite une clé administrateur.",
  MODELE_INDISPONIBLE: "Le modèle est indisponible.",
};

export function messageErreur(corps, status) {
  const code = corps?.erreur?.code;
  return MESSAGES[code] ?? `Erreur de l'API (${status}).`;
}

function urlBase(apiUrl) {
  return apiUrl.trim().replace(/\/+$/, "");
}

function entetes(cle) {
  return { "X-API-Key": cle.trim() };
}

export async function sante(apiUrl, cle, fetcher = fetch) {
  const response = await fetcher(`${urlBase(apiUrl)}/v1/health`, {
    headers: entetes(cle),
  });
  if (!response.ok) {
    throw new Error(messageErreur(await response.json().catch(() => ({})), response.status));
  }
  return response.json();
}

export async function predire(apiUrl, cle, text, fetcher = fetch) {
  const response = await fetcher(`${urlBase(apiUrl)}/v1/predict`, {
    method: "POST",
    headers: { ...entetes(cle), "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) {
    throw new Error(messageErreur(await response.json().catch(() => ({})), response.status));
  }
  return response.json();
}
