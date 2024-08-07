import { writable } from "svelte/store";

export const id = writable<string | null>(null);
export const role = writable<string | null>(null);
export const mode = writable<string | null>(null);
export const userMode = writable<string | null>(null);

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

export const setId = (newId: string | null) => {
  id.set(newId);
};

export const setRole = (newRole: string | null) => {
  role.set(newRole);
};

export const setMode = (newMode: string | null) => {
  mode.set(newMode);
};

export const setUserMode = (newMode: string | null) => {
  userMode.set(newMode);
};
