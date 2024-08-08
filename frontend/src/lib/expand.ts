// src/lib/expand.ts
import { writable } from 'svelte/store';

const initialExpandedNodes = new Map<string, boolean>();

export const expandedNodes = writable(initialExpandedNodes);

export function resetNodes() {
  expandedNodes.set(new Map<string, boolean>());
}

export function addNode(url: string) {
  expandedNodes.update(map => {
    map.set(url, true);
    return new Map(map);
  });
}

export function removeNode(url: string) {
  expandedNodes.update(map => {
    map.delete(url);
    return new Map(map);
  });
}

export function toggleNode(url: string) {
  expandedNodes.update(map => {
    if (map.has(url)) {
      map.set(url, !map.get(url));
    } else {
      map.set(url, true);
    }
    return new Map(map);
  });
}
