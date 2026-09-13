const REPO = "SamoTech/RepoSource-Registry";
const RAW_BASE = `https://raw.githubusercontent.com/${REPO}/main`;

export async function getJson(path) {
  const response = await fetch(`${RAW_BASE}/${path}`, { next: { revalidate: 3600 } });
  if (!response.ok) throw new Error(`Unable to load ${path}: ${response.status}`);
  return response.json();
}

export async function getStats() {
  return getJson("data/statistics.json");
}

export async function getDataset() {
  return getJson("data/repositories.json");
}

export function normalizeQuery(value) {
  return (value || "").trim().toLowerCase();
}

export function searchRepositories(records, { q = "", language = "", category = "", minStars = "" } = {}) {
  const query = normalizeQuery(q);
  const lang = normalizeQuery(language);
  const cat = normalizeQuery(category);
  const threshold = Number(minStars) || 0;

  return records
    .filter((repo) => {
      if (threshold && repo.stars < threshold) return false;
      if (lang && normalizeQuery(repo.primary_language) !== lang) return false;
      if (cat && !(repo.categories || []).some((item) => normalizeQuery(item) === cat)) return false;
      if (!query) return true;
      const haystack = [repo.full_name, repo.owner, repo.name, repo.description, repo.primary_language, ...(repo.topics || [])]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return haystack.includes(query);
    })
    .sort((a, b) => b.stars - a.stars || a.full_name.localeCompare(b.full_name))
    .slice(0, 100);
}

export function findRepository(records, owner, name) {
  const target = `${owner}/${name}`.toLowerCase();
  return records.find((repo) => String(repo.full_name).toLowerCase() === target);
}
