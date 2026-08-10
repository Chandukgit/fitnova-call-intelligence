import apiClient from "./apiClient";

const tokenKey = "fitnova_access_token";
const userKey = "fitnova_current_user";

const nameOf = (person) => person ? `${person.first_name} ${person.last_name}` : "Unknown";
const recommendationList = (recommendation) => recommendation ? recommendation.split("\n").filter(Boolean) : [];

export async function login(email, password, rememberMe = false) {
  const { data } = await apiClient.post("/auth/login", { email, password });
  const storage = rememberMe ? localStorage : sessionStorage;
  storage.setItem(tokenKey, data.access_token);
  localStorage.setItem(tokenKey, data.access_token);
  const user = await getCurrentUser();
  return user;
}

export async function getCurrentUser() {
  const { data } = await apiClient.get("/users/me");
  localStorage.setItem(userKey, JSON.stringify(data));
  return data;
}

export function getStoredUser() {
  try { return JSON.parse(localStorage.getItem(userKey)); } catch { return null; }
}

export function logout() {
  localStorage.removeItem(tokenKey);
  sessionStorage.removeItem(tokenKey);
  localStorage.removeItem(userKey);
}

export const getOrganizations = () => apiClient.get("/organizations").then(({ data }) => data);
export const getTeams = () => apiClient.get("/teams").then(({ data }) => data);
export const getAdvisors = () => apiClient.get("/advisors").then(({ data }) => data);
export const getCustomers = () => apiClient.get("/customers").then(({ data }) => data);
export const getCallsRaw = () => apiClient.get("/calls").then(({ data }) => data);
export const getTranscriptsRaw = () => apiClient.get("/transcripts").then(({ data }) => data);
export const getAnalysesRaw = () => apiClient.get("/analysis").then(({ data }) => data);
export const getIssueTagsRaw = () => apiClient.get("/issue-tags").then(({ data }) => data);
export const getFeedbackRaw = () => apiClient.get("/feedback").then(({ data }) => data);

export async function getCallData() {
  const [calls, customers, advisors, analyses] = await Promise.all([
    getCallsRaw(), getCustomers(), getAdvisors(), getAnalysesRaw(),
  ]);
  const customerById = new Map(customers.map((customer) => [String(customer.id), customer]));
  const advisorById = new Map(advisors.map((advisor) => [String(advisor.id), advisor]));
  const analysisByCall = new Map(analyses.map((analysis) => [String(analysis.call_id), analysis]));
  return calls.map((call) => ({
    ...call,
    customerName: nameOf(customerById.get(String(call.customer_id))),
    advisorName: nameOf(advisorById.get(String(call.advisor_id))),
    date: call.created_at,
    score: analysisByCall.get(String(call.id))?.overall_score ?? null,
    status: call.call_status,
  }));
}

export async function getCallDetails(callId) {
  const [calls, customers, advisors, transcripts, analyses, tags, feedback] = await Promise.all([
    getCallsRaw(), getCustomers(), getAdvisors(), getTranscriptsRaw(), getAnalysesRaw(), getIssueTagsRaw(), getFeedbackRaw(),
  ]);
  const call = calls.find((item) => String(item.id) === String(callId));
  if (!call) return null;
  const analysis = analyses.find((item) => String(item.call_id) === String(call.id)) || null;
  const transcript = transcripts.find((item) => String(item.call_id) === String(call.id)) || null;
  const messages = transcript ? [{ speaker: "advisor", time: "", text: transcript.transcript }] : [];
  return {
    call: {
      ...call,
      customer: customers.find((item) => String(item.id) === String(call.customer_id)),
      advisor: advisors.find((item) => String(item.id) === String(call.advisor_id))
    },
    transcript: messages,
    analysis: analysis && {
      ...analysis,
      overallScore: analysis.overall_score,
      communication: analysis.needs_discovery_score,
      compliance: analysis.compliance_score,
      productKnowledge: analysis.product_knowledge_score,
      customerSatisfaction: analysis.customer_sentiment,
      recommendations: recommendationList(analysis.recommendation),
    },
    tags: analysis ? tags.filter((item) => String(item.analysis_id) === String(analysis.id)) : [],
    feedback: analysis ? feedback.filter((item) => String(item.analysis_id) === String(analysis.id)) : [],
  };
}

export async function getAnalytics() {
  const [calls, analyses, teams, advisors] = await Promise.all([getCallsRaw(), getAnalysesRaw(), getTeams(), getAdvisors()]);
  const analysisByCall = new Map(analyses.map((item) => [item.call_id, item]));
  const byDay = new Map();
  calls.forEach((call) => {
    const day = new Date(call.created_at).toLocaleDateString("en-US", { weekday: "short" });
    byDay.set(day, (byDay.get(day) || 0) + 1);
  });
  const averageFor = (advisorIds) => {
    const scores = calls.filter((call) => advisorIds.includes(call.advisor_id)).map((call) => analysisByCall.get(call.id)?.overall_score).filter(Number.isFinite);
    return scores.length ? Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length) : 0;
  };
  return {
    weeklyCallVolume: [...byDay].map(([day, count]) => ({ day, calls: count })),
    scoreTrend: [{ month: "Current", avgScore: averageFor(advisors.map((advisor) => advisor.id)) }],
    teamComparison: teams.map((team) => ({ team: team.name, score: averageFor(advisors.filter((advisor) => advisor.team_id === team.id).map((advisor) => advisor.id)) })),
    complianceBreakdown: ["COMPLETED", "PENDING", "FAILED"].map((status) => ({ name: status, value: calls.filter((call) => call.call_status === status).length })),
  };
}

export async function uploadAudio({ advisorId, customerId, file }) {
  const form = new FormData();
  form.append("advisor_id", advisorId);
  form.append("customer_id", customerId);
  form.append("file", file);
  const { data } = await apiClient.post("/upload/audio", form, { headers: { "Content-Type": "multipart/form-data" } });
  return data;
}
