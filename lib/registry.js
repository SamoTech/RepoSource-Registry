import { cache } from "react";

const REPO = "SamoTech/RepoSource-Registry";
const RAW_BASE = `https://raw.githubusercontent.com/${REPO}/main`;

export const getJson = cache(async function getJson(path) {
  const response = await fetch(`${RAW_BASE}/${path}`, { next: { revalidate: 3600 } });
  if (!response.ok) throw new Error(`Unable to load ${path}: ${response.status}`);
  return response.json();
});

export const getStats = cache(async function getStats() {
  return getJson("data/statistics.json");
});

export const getDataset = cache(async function getDataset() {
  return getJson("data/repositories.json");
});

export function normalizeQuery(value) {
  return String(value || "").trim().toLowerCase();
}

function numericStars(repo) {
  const value = Number(repo?.stars);
  return Number.isFinite(value) ? value : 0;
}

function repositoryName(repo) {
  return String(repo?.full_name || `${repo?.owner || ""}/${repo?.name || ""}`).trim();
}

export function searchRepositories(
  records,
  { q = "", language = "", category = "", topic = "", minStars = "", sort = "stars" } = {},
) {
  const query = normalizeQuery(q);
  const lang = normalizeQuery(language);
  const cat = normalizeQuery(category);
  const topicQuery = normalizeQuery(topic);
  const threshold = Number(minStars) || 0;
  const source = Array.isArray(records) ? records : [];

  return source
    .filter((repo) => {
      if (!repo || typeof repo !== "object") return false;
      if (threshold && numericStars(repo) < threshold) return false;
      if (lang && normalizeQuery(repo.primary_language) !== lang) return false;
      if (cat && !(Array.isArray(repo.categories) ? repo.categories : []).some((item) => normalizeQuery(item) === cat)) return false;
      if (topicQuery && !(Array.isArray(repo.topics) ? repo.topics : []).some((item) => normalizeQuery(item) === topicQuery)) return false;
      if (!query) return true;
      const haystack = [
        repo.full_name,
        repo.owner,
        repo.name,
        repo.description,
        repo.primary_language,
        ...(Array.isArray(repo.topics) ? repo.topics : []),
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return haystack.includes(query);
    })
    .sort((a, b) => {
      if (sort === "name") return repositoryName(a).localeCompare(repositoryName(b), undefined, { sensitivity: "base" });
      if (sort === "stars-asc") return numericStars(a) - numericStars(b) || repositoryName(a).localeCompare(repositoryName(b));
      return numericStars(b) - numericStars(a) || repositoryName(a).localeCompare(repositoryName(b));
    })
    .slice(0, 100);
}

export function findRepository(records, owner, name) {
  const target = `${decodeURIComponent(owner || "")}/${decodeURIComponent(name || "")}`.toLowerCase();
  return (Array.isArray(records) ? records : []).find((repo) => repositoryName(repo).toLowerCase() === target);
}

export function isSafeGithubUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" && (url.hostname === "github.com" || url.hostname.endsWith(".github.com"));
  } catch {
    return false;
  }
}
