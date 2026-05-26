const API_BASE = import.meta.env.VITE_API_BASE_URL ?? `${window.location.protocol}//${window.location.hostname}:18000`;

async function req(path: string, init?: RequestInit) {
  const r = await fetch(`${API_BASE}${path}`, init);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export const api = {
  login: (username: string, password: string) => req('/auth/login', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ username, password }) }),
  listEntities: (campaignId: number, p: Record<string, string>) => req(`/campaigns/${campaignId}/entities?${new URLSearchParams(p)}`),
  getEntityDetail: (id: string) => req(`/entities/${id}/detail`),
  getEntity: (id: string) => req(`/entities/${id}`),
  createEntity: (payload: any) => req('/entities', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(payload) }),
  updateEntity: (id: string, payload: any) => req(`/entities/${id}`, { method: 'PUT', headers: { 'content-type': 'application/json' }, body: JSON.stringify(payload) }),
  deleteEntity: (id: number) => req(`/entities/${id}`, { method: 'DELETE' }),
  listTags: (campaignId: number) => req(`/campaigns/${campaignId}/tags`),
  listRelationships: (campaignId: number) => req(`/campaigns/${campaignId}/relationships`),
  listEvents: (campaignId: number) => req(`/campaigns/${campaignId}/events`),
  foundryStatus: () => req('/foundry/status')
};
