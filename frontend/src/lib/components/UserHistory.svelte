<script lang="ts">
  import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
  } from "flowbite-svelte";
  import { getId } from "$lib/store";
  import { onMount } from "svelte";
  import fastapi from "$lib/fastapi";

  interface LogEntry {
    time: string;
    main_url: string;
    status: string;
    file?: string;
    _id: string;
  }

  let logs: LogEntry[] = [];

  let filteredLogs: LogEntry[] = [...logs];
  let dateFilter: string = "";
  let urlFilter: string = "";
  let statusFilter: string = "";

  async function downloadReport(log: LogEntry) {
    try {
      const response = await new Promise<Response>((resolve, reject) => {
        fastapi("GET", `/report/${log.file}`, {}, resolve, reject);
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

  function filterLogs() {
    filteredLogs = logs.filter((log) => {
      return (
        (!dateFilter || log.time.includes(dateFilter)) &&
        (!urlFilter ||
          log.main_url.toLowerCase().includes(urlFilter.toLowerCase())) &&
        (!statusFilter ||
          log.status.toLowerCase().includes(statusFilter.toLowerCase()))
      );
    });
  }

  async function fetchLogs(user_id: string) {
    try {
      const response = await new Promise<any>((resolve, reject) => {
        fastapi(
          "GET",
          `/history/${user_id}`,
          {},
          (data) => resolve(data),
          (error) => reject(error)
        );
      });

      logs = response;
      filteredLogs = [...logs];
    } catch (err) {
      console.error("Error getting history: ", err);
    }
  }

  async function deleteLog(history_id: string) {
    try {
      await new Promise<void>((resolve, reject) => {
        fastapi(
          "DELETE",
          `/history/${getId()}/${history_id}`,
          {},
          () => resolve(),
          (error) => reject(error)
        );
      });

      logs = logs.filter((log) => log._id !== history_id);
      filteredLogs = [...logs];
    } catch (err) {
      console.error("Error deleting log: ", err);
    }
  }

  onMount(() => {
    const user_id = getId();
    if (user_id) {
      fetchLogs(user_id);
    } else {
      console.error("User ID not found");
    }
  });
</script>

<div class="flex w-full select-none h-full bg-gray-50">
  <div class="w-full p-6">
    <div class="flex items-center mb-6">
      <div
        class="w-full bg-white shadow-md rounded-lg p-1.5 flex items-center space-x-4"
      >
        <span class="text-lg font-semibold">Filter:</span>
        <input
          type="text"
          placeholder="Date"
          bind:value={dateFilter}
          on:input={filterLogs}
          class="border rounded px-3 py-2 text-sm 4xl:text-lg shadow-sm"
        />
        <input
          type="text"
          placeholder="URL"
          bind:value={urlFilter}
          on:input={filterLogs}
          class="border rounded px-3 py-2 text-sm 4xl:text-lg shadow-sm"
        />
      </div>
    </div>
    <Table shadow>
      <TableHead class="text-center text-sm 4xl:text-lg">
        <TableHeadCell>DATE</TableHeadCell>
        <TableHeadCell>URL</TableHeadCell>
        <TableHeadCell>STATUS</TableHeadCell>
        <TableHeadCell>REPORT</TableHeadCell>
        <TableHeadCell>ACTION</TableHeadCell>
      </TableHead>
      <TableBody tableBodyClass="divide-y">
        {#each filteredLogs as log}
          <TableBodyRow class="text-center 4xl:text-lg">
            <TableBodyCell>{log.time}</TableBodyCell>
            <TableBodyCell>{log.main_url}</TableBodyCell>
            <TableBodyCell class={`${log.status === "Test Completed" ? "text-green-500" : "text-red-500"}`}>
              {log.status}
            </TableBodyCell>
              <TableBodyCell
                ><button
                  on:click={() => downloadReport(log)}
                  class="text-gray-500 disabled:text-blue-700 cursor-not-allowed disabled:cursor-pointer"
                  disabled={log.file !== null}>Download</button
                ></TableBodyCell
              >
            <TableBodyCell
              ><button class="text-red-500" on:click={() => deleteLog(log._id)}
                >Delete</button
              ></TableBodyCell
            >
          </TableBodyRow>
        {/each}
      </TableBody>
    </Table>
  </div>
</div>
