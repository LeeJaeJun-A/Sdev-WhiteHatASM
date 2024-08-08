import { writable } from "svelte/store";

export const urlCVE = writable<string[]>([]);

export const toggleCveForUrl = (url: string, cve: string) => {
  urlCVE.update((list) => {
    const pairToToggle = `${url} ${cve}`;
    if (list.includes(pairToToggle)) {
      return list.filter((pair) => pair !== pairToToggle);
    } else {
      return [...list, pairToToggle];
    }
  });
};

export const resetUrlCVE = () => {
  urlCVE.set([]);
}