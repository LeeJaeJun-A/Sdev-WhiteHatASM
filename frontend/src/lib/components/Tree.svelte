<script lang="ts">
  import { onDestroy } from "svelte";
  import { expandedNodes, toggleNode } from "$lib/expand";
  import { toggleCveForUrl } from "$lib/selectCVE";

  interface TreeNode {
    url: string;
    cve: string[];
    children: TreeNode[];
  }

  export let data: TreeNode;

  let isExpanded = false;

  let unsubscribe: () => void;

  $: {
    unsubscribe = expandedNodes.subscribe((map) => {
      isExpanded = map.get(data.url) || false;
    });
  }

  function handleToggle() {
    toggleNode(data.url);
  }

  function handleCveToggle(cve: string) {
    toggleCveForUrl(data.url, cve);
  }

  onDestroy(() => {
    if (unsubscribe) {
      unsubscribe();
    }
  });
</script>

<div class="ml-4">
  {#if data}
    <div class="mb-2">
      <button
        class="flex items-center bg-blue-100 text-blue-800 border border-blue-300 p-2 rounded-md text-sm font-medium hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
        on:click={handleToggle}
      >
        <span class="truncate flex-1 4xl:text-xl">📄 {data.url}</span>
        <svg
          class="w-4 h-4 ml-2 transition-transform duration-200"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          class:rotate-180={isExpanded}
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {#if isExpanded && data.cve.length > 0}
        <div
          class="ml-4 mt-1 transition duration-200 ease-in-out transform scale-95"
        >
          {#each data.cve as cve}
            <div class="mb-1">
              <button
                class="flex items-center bg-red-100 text-red-800 border border-red-300 p-2 rounded-md text-sm font-medium hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 transition duration-200 mb-1"
                on:click={()=>handleCveToggle(cve)}
                >
                <span class="truncate flex-1 4xl:text-xl">💣 {cve}</span>
              </button>
            </div>
          {/each}
        </div>
      {/if}

      {#if isExpanded && data.children.length > 0}
        <div
          class="mt-1 transition duration-200 ease-in-out transform scale-95"
        >
          {#each data.children as child}
            <svelte:self data={child} />
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .rotate-180 {
    transform: rotate(180deg);
  }
</style>
