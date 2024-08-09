import { writable } from "svelte/store";

export const id = writable<string | null>(null);
export const role = writable<string | null>(null);
export const mode = writable<string | null>(null);
export const userMode = writable<string | null>(null);
export const currentUrl = writable<string | null>(null);
export const crawlResult = writable<any>(null);
export const reportName = writable<string | null>(null);
export const historyID = writable<string | null>(null);

export const getId = () => {
  let currentId: string | null = null;
  id.subscribe((value) => (currentId = value))();
  return currentId;
};

export const getRole = () => {
  let currentRole: string | null = null;
  role.subscribe((value) => (currentRole = value))();
  return currentRole;
};

export const getCurrentUrl = () => {
  let tempUrl: string | null = null;
  currentUrl.subscribe((value) => (tempUrl = value))();
  return tempUrl;
};

export const getCrawlResult = () => {
  let currentCrawlResult: any = null;
  crawlResult.subscribe((value) => (currentCrawlResult = value))();
  return currentCrawlResult;
};

export const getreportName = () => {
  let currentReportName: any = null;
  reportName.subscribe((value) => (currentReportName = value))();
  return currentReportName;
};

export const getHistoryID = () => {
  let currentHistoryID: any = null;
  historyID.subscribe((value) => (currentHistoryID = value))();
  return currentHistoryID;
};

export const setId = (newId: string | null) => {
  id.set(newId);
};

export const setRole = (newRole: string | null) => {
  role.set(newRole);
};

export const setMode = (newMode: string | null) => {
  mode.set(newMode);
};

export const setUserMode = (newUserMode: string | null) => {
  userMode.set(newUserMode);
};

export const setCurrentUrl = (newUrl: string | null) => {
  currentUrl.set(newUrl);
};

export const setCrawlResult = (newCrawlResult: any) => {
  crawlResult.set(newCrawlResult);
};

export const setReportName = (newReportName: any) => {
  reportName.set(newReportName);
};

export const setHistoryID = (newHistoryID: any) => {
  historyID.set(newHistoryID);
};