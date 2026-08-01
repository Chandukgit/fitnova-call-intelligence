// This file pretends to be an API layer.
// Every function returns a Promise, just like a real API call would.
// Later, you can replace the inside of each function with an axios call
// (using apiClient.js) and the rest of the app won't need to change.

import organizations from "../mock/organizations.json";
import teams from "../mock/teams.json";
import advisors from "../mock/advisors.json";
import calls from "../mock/calls.json";
import transcripts from "../mock/transcripts.json";
import scores from "../mock/scores.json";
import issueTags from "../mock/issueTags.json";
import analytics from "../mock/analytics.json";

// Small helper to fake network delay
function fakeDelay(data, ms = 300) {
  return new Promise((resolve) => setTimeout(() => resolve(data), ms));
}

export function getOrganization() {
  return fakeDelay(organizations);
}

export function getTeams() {
  return fakeDelay(teams);
}

export function getAdvisors() {
  return fakeDelay(advisors);
}

export function getCalls() {
  return fakeDelay(calls);
}

export function getCallById(callId) {
  const call = calls.find((c) => c.id === callId);
  return fakeDelay(call);
}

export function getTranscript(callId) {
  return fakeDelay(transcripts[callId] || []);
}

export function getScores(callId) {
  return fakeDelay(scores[callId] || null);
}

export function getIssueTags(callId) {
  return fakeDelay(issueTags[callId] || []);
}

export function getAnalytics() {
  return fakeDelay(analytics);
}
