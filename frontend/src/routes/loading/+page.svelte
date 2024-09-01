<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { goto } from "$app/navigation";
  import { getCurrentUrl, getId, setCrawlResult } from "$lib/store";
  import fastapi from "$lib/fastapi";

  let socket: WebSocket | null = null;
  let currentMessage: string = "Please Wait";
  let isLoading = true;

  const baseUrl = import.meta.env.VITE_FASTAPI_URL || "http://127.0.0.1:8000";

  async function connectWebSocket() {
    return new Promise<void>((resolve, reject) => {
      const socketUrl = `ws://${baseUrl.replace(/^http:\/\/|^https:\/\//, "")}/api/ws/${getId()}`;
      socket = new WebSocket(socketUrl);

      socket.onopen = () => {
        resolve();
      };

      socket.onmessage = async (event) => {
        const message = event.data;
        if (message === "Full crawling completed") {
          isLoading = false;
        } else if (message.startsWith("{") && message.endsWith("}")) {
          try {
            setCrawlResult(JSON.parse(message));
            goto("/test", {replaceState:true});
          } catch (error) {
            console.error("Failed to parse JSON:", error);
            goto("/user", {replaceState:true});
          }
        } else {
          currentMessage = message;
        }
      };

      socket.onerror = (error) => {
        reject(error);
      };
    });
  }

  async function startCrawling() {
    try {
      await connectWebSocket();
      const url = getCurrentUrl();
      const id = getId();
      const params = { url, id };
      fastapi(
        "POST",
        "/api/crawl",
        params,
        (response) => {
          console.log("Crawling started: ", response);
        },
        (error) => {
          console.error("Error starting crawling: ", error);
        }
      );
    } catch (error) {
      console.error("Failed to connect to WebSocket:", error);
    }
  }
  
  onMount(async () => {
    await startCrawling();
  });

  onDestroy(() => {
    if (socket) {
      socket.close();
    }
  });

  function goBack() {
    goto("/user", { replaceState: true });
  }
</script>

<div class="flex flex-col justify-center items-center h-screen bg-gray-50">
  <div class="relative flex flex-col justify-center items-center w-full h-full">
    <div class="relative flex justify-center items-center w-full h-full">
      {#each Array(6).fill(0) as _, i}
        <div
          class="absolute w-15 h-15 animate-rotate 4xl:w-32 4xl:h-32"
          style="animation-delay: {0.15 * i}s;"
        >
          <div class="relative top-7 w-2.5 h-2.5 rounded-full bg-red-500 4xl:w-4 4xl:h-4"></div>
        </div>
      {/each}
    </div>
    <div class="absolute bottom-0 mb-12 flex flex-col justify-center items-center text-black 4xl:mb-24 select-none">
      {#if isLoading}
        {#if currentMessage}
          <p class="text-sm 4xl:text-xl">{currentMessage}</p>
        {/if}
      {/if}
      <button
        on:click={goBack}
        class="mt-4 px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-blue-300 4xl:mt-8 4xl:w-40 4xl:h-16 4xl:text-xl"
      >
        크롤링 취소
      </button>
    </div>
  </div>
</div>

<style>
  @keyframes rotate {
    30% {
      transform: rotate(220deg);
    }
    40% {
      transform: rotate(450deg);
    }
    75% {
      transform: rotate(720deg);
      opacity: 1;
    }
    76% {
      opacity: 0;
    }
    100% {
      transform: rotate(0deg);
      opacity: 0;
    }
  }

  .animate-rotate {
    animation: rotate 2s linear infinite;
  }
</style>