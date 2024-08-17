<script lang="ts">
  import { goto } from "$app/navigation";
  import { initializeSession } from "$lib/auth";
  import {
    getCrawlResult,
    getId,
    setReportID,
    getReportID,
    getHistoryID,
    getCurrentUrl,
    setHistoryID
  } from "$lib/store";
  import { onMount, onDestroy } from "svelte";
  import { resetNodes } from "$lib/expand";
  import { urlCVE, toggleCveForUrl, resetUrlCVE } from "$lib/selectCVE";
  import { writable, get } from "svelte/store";
  import Swal from "sweetalert2";
  import Tree from "$lib/components/Tree.svelte";
  import fastapi from "$lib/fastapi";

  interface HistoryResponse {
    history_id: string;
    status: string;
  }

  let socket: WebSocket | null = null;
  let crawlResult: any = null;
  let urlCvePairs: { url: string; cve: string }[] = [];
  let unsubscribe: () => void;
  let progressPercentage = writable<number>(0);
  let logMessages = writable<string[]>([]);
  let totalCVE: number = 0;
  let completedCVE: number = 0;
  let isTestStarted = writable<boolean>(false);
  let isTestCompleted = writable<boolean>(false);

  const baseUrl = import.meta.env.VITE_FASTAPI_URL || "http://127.0.0.1:8000";

  async function connectWebSocket() {
    return new Promise<void>((resolve, reject) => {
      const socketUrl = `ws://${baseUrl.replace(/^http:\/\/|^https:\/\//, "")}/ws/${getId()}`;
      console.log("Connecting to WebSocket URL: ", socketUrl);
      socket = new WebSocket(socketUrl);

      socket.onopen = () => {
        resolve();
      };

      socket.onmessage = async (event) => {
        const message = event.data;
        console.log("Received WebSocket message:", message);
        if (message.startsWith("Testing") && message.endsWith("completed.")) {
          completedCVE++;
          const percentage = Math.min(
            Math.floor((completedCVE / (totalCVE + 1)) * 100),
            100
          );
          progressPercentage.set(percentage);
        } else if (message.startsWith("The report")) {
          const reportTitleMatch = message.match(
            /The report '(.*?)' has been completed\./
          );
          
          if (reportTitleMatch && reportTitleMatch[1]) {
            progressPercentage.set(100);
            const reportID = reportTitleMatch[1];
            setReportID(reportID);

            await new Promise((resolve, reject) => {
              fastapi(
                "PUT",
                `/api/history/${getId()}/${getHistoryID()}`,
                { file: reportID },
                resolve,
                reject
              );
            });
          }
        }

        logMessages.update((messages) => [...messages, message]);

        if (message === "Completing the test.") {
          isTestStarted.set(false);
          isTestCompleted.set(true);

          await new Promise((resolve, reject) => {
            fastapi(
              "PUT",
              `/api/history/${getId()}/${getHistoryID()}`,
              { status: "Test Completed" },
              resolve,
              reject
            );
          });

          if (socket) {
            socket.close();
            socket = null;
          }
        }
      };

      socket.onclose = () => {
        console.log("WebSocket connection closed");
      };

      socket.onerror = (error) => {
        console.error("WebSocket error", error);
        reject(error);
      };
    });
  }

  async function startTest() {
    try {
      const urlCVEList = get(urlCVE);
      const id = getId();
      totalCVE = urlCVEList.length;
      if (totalCVE === 0) {
        Swal.fire({
          icon: "error",
          title: "Please Select CVEs",
          text: "CVE를 한 개 이상 선택해주세요.",
        });
        return;
      }

      completedCVE = 0;
      progressPercentage.set(0);
      logMessages.set(["Test started..."]);
      isTestStarted.set(true);
      isTestCompleted.set(false);
      await connectWebSocket();

      await new Promise((resolve, reject) => {
        fastapi("POST", "/api/test", { urlCVEList, id }, resolve, reject);
      });

      const now = new Date().toISOString();
      const historyResponse = await new Promise<HistoryResponse>(
        (resolve, reject) => {
          fastapi(
            "POST",
            "/api/history",
            {
              user_id: getId(),
              history: {
                time: now,
                main_url: getCurrentUrl(),
                status: "Test Started",
              },
            },
            resolve,
            reject
          );
        }
      );

      setHistoryID(historyResponse.history_id);
    } catch (error) {
      console.error("Failed to connect to WebSocket:", error);
    }
  }

  function handleRemoveCve(url: string, cve: string) {
    toggleCveForUrl(url, cve);
  }

  function handleTestCancel() {
    Swal.fire({
      icon: "warning",
      title: "Are you sure?",
      html: "검사를 취소하고, 메인화면으로 돌아가시겠습니까?",
      showCancelButton: true,
      confirmButtonText: "Yes",
      cancelButtonText: "No",
      reverseButtons: true,
      customClass: {
        confirmButton: "swal-button",
        cancelButton: "swal-button",
      },
      buttonsStyling: false,
    }).then((result) => {
      if (result.isConfirmed) {
        goto("/user", { replaceState: true });
      }
    });
  }

  async function handleCancelDuringTest() {
    try {
      const result = await Swal.fire({
        icon: "warning",
        title: "Are you sure?",
        html: "지금까지의 검사 내용을 모두 잃게 됩니다.<br>정말 검사를 종료하시겠습니까?",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "No",
        reverseButtons: true,
        customClass: {
          confirmButton: "swal-button",
          cancelButton: "swal-button",
        },
        buttonsStyling: false,
      });

      if (result.isConfirmed) {
        if (socket) {
          socket.close();
          socket = null;
        }

        await new Promise((resolve, reject) => {
          fastapi(
            "PUT",
            `/api/history/${getId()}/${getHistoryID()}`,
            { status: "Test Canceled" },
            resolve,
            reject
          );
        });

        logMessages.set([]);

        completedCVE = 0;
        totalCVE = 0;
        isTestStarted.set(false);
        isTestCompleted.set(false);
      }
    } catch (error) {
      console.error("Error during cancel operation:", error);
    }
  }

  async function downloadReport() {
    try {
      const response = await new Promise<Response>((resolve, reject) => {
        fastapi("GET", `/api/report/${getReportID()}`, {}, resolve, reject);
      });

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;

      document.body.appendChild(a);
      a.click();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  }

  onMount(() => {
    initializeSession();
    crawlResult = getCrawlResult();
    resetNodes();
    resetUrlCVE();

    unsubscribe = urlCVE.subscribe((list) => {
      urlCvePairs = list.map((item) => {
        const [url, cve] = item.split(" ", 2);
        return { url, cve };
      });
    });
  });

  onDestroy(() => {
    if (unsubscribe) {
      unsubscribe();
    }
  });
</script>

<main class="h-screen w-screen bg-gray-50 flex select-none">
  <div id="tree" class="h-full w-1/2 p-4">
    <div
      class="h-full w-full shadow-md border rounded-lg overflow-auto pt-4 flex flex-col items-start bg-white"
    >
      {#if crawlResult}
        <Tree data={crawlResult} />
      {:else}
        <p class="w-full h-full flex justify-center items-center 4xl:text-xl">
          가능한 CVE가 없습니다.
        </p>
      {/if}
    </div>
  </div>
  <div id="test" class="h-full w-1/2 p-4">
    <div id="select" class="flex w-full flex-col" style="height: 37%;">
      <p
        class="w-full flex p-1 justify-center items-center border border-b-0 rounded-t-lg bg-gray-200 4xl:text-2xl"
      >
        선택된 CVE 목록
      </p>
      <div
        class="h-full w-full border bg-white shadow-md rounded-b-lg overflow-auto"
      >
        <table class="w-full text-sm 4xl:text-xl">
          <tbody>
            {#each urlCvePairs as { url, cve }}
              <tr>
                <td class="border-b p-2">{url}</td>
                <td class="border-b p-2 min-w-32">{cve}</td>
                <td class="border-b p-2 text-center">
                  <button
                    class="text-red-500 hover:text-red-700"
                    on:click={() => handleRemoveCve(url, cve)}
                  >
                    ❌
                  </button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
    <div
      id="progressbar"
      class="flex justify-center items-center w-full"
      style="height: 10%;"
    >
      <div class="w-full h-4 bg-gray-200 rounded-full 4xl:h-8">
        <div
          class="h-4 bg-green-400 rounded-full flex justify-center items-center 4xl:h-8 4xl:text-xl"
          style="width: {$progressPercentage}%"
        >
          {#if $progressPercentage > 0}
            {$progressPercentage}%
          {/if}
        </div>
      </div>
    </div>

    <div id="log" class="flex w-full flex-col" style="height: 43%;">
      <p
        class="w-full flex p-1 justify-center items-center border border-b-0 rounded-t-lg bg-gray-200 4xl:text-2xl"
      >
        검사 로그
      </p>
      <div
        class="h-full w-full border bg-white shadow-md rounded-b-lg overflow-auto"
      >
        {#each $logMessages as message}
          <p class="p-2 border-b text-sm 4xl:text-xl">{message}</p>
        {/each}
      </div>
    </div>
    <div
      id="button"
      class="flex justify-center items-end w-full"
      style="height: 10%;"
    >
      <div
        class="w-full h-3/4 flex justify-center items-center space-x-2 4xl:space-x-10"
      >
        {#if $isTestStarted}
          <button
            class="h-2/3 w-1/4 border px-2 py-1 bg-orange-500 rounded-lg text-white hover:bg-orange-600 4xl:rounded-2xl 4xl:text-xl"
            on:click={handleCancelDuringTest}
            disabled={$isTestCompleted}
          >
            검사 중지
          </button>
        {:else}
          <button
            class="h-2/3 w-1/4 border px-2 py-1 bg-orange-500 rounded-lg text-white hover:bg-orange-600 4xl:rounded-2xl 4xl:text-xl"
            on:click={handleTestCancel}
          >
            검사 취소
          </button>
        {/if}
        <button
          class="h-2/3 w-1/4 border px-2 py-1 bg-green-500 rounded-lg text-white hover:bg-green-600 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed 4xl:rounded-2xl 4xl:text-xl"
          on:click={startTest}
          disabled={$isTestStarted}
        >
          검사 시작
        </button>
        <button
          class="h-2/3 w-1/4 border px-2 py-1 bg-blue-500 rounded-lg text-white hover:bg-blue-600 disabled:bg-gray-400 disabled:border-gray-400 disabled:cursor-not-allowed 4xl:rounded-2xl 4xl:text-xl"
          disabled={!$isTestCompleted}
          on:click={downloadReport}
        >
          보고서 받기
        </button>
      </div>
    </div>
  </div>
</main>

<style>
  :global(.swal-button) {
    padding: 7px 14px;
    min-width: 100px;
    border-radius: 5px;
    font-size: 18px;
    font-weight: bold;
    margin-right: 10px;
  }

  :global(.swal-button.swal2-confirm) {
    background-color: #3085d6; /* Default confirm button color */
    color: white;
  }

  :global(.swal-button.swal2-cancel) {
    background-color: #f97316; /* Custom cancel button color */
    color: white;
  }

  :global(.swal-button:hover) {
    filter: brightness(0.9);
  }
</style>
