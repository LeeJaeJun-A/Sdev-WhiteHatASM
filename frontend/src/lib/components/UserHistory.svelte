<script lang="ts">
  import {
    Table,
    TableHead,
    TableHeadCell,
    TableBody,
    TableBodyRow,
    TableBodyCell,
  } from "flowbite-svelte";
  import { onMount } from "svelte";
  import { getId } from "$lib/store";
  import fastapi from "$lib/fastapi";
  import { format } from "date-fns";

  interface LogEntry {
    time: string;
    main_url: string;
    status: string;
    file?: string;
    _id: string;
  }

  let logs: LogEntry[] = [];
  let filteredLogs: LogEntry[] = [...logs];
  let dateFrom: string = "";
  let dateTo: string = "";
  let urlFilter: string = "";
  let statusFilter: string = "";

  async function downloadReport(log: LogEntry) {
    try {
      const response = await new Promise<Response>((resolve, reject) => {
        fastapi("GET", `/api/report/${log.file}`, {}, resolve, reject);
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

  function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return format(date, "yyyy-MM-dd HH:mm:ss");
  }

  function syncDates() {
    if (dateFrom && !dateTo) {
      dateTo = dateFrom;
    } else if (!dateFrom && dateTo) {
      dateFrom = dateTo;
    } else if (dateFrom && dateTo && new Date(dateFrom) > new Date(dateTo)) {
      dateFrom = dateTo;
    }
  }

  function filterLogs() {
    syncDates();
    filteredLogs = logs.filter((log) => {
      const logDate = new Date(log.time);
      const fromDate = new Date(dateFrom);
      const toDate = new Date(dateTo);

      return (
        (!dateFrom || logDate >= fromDate) &&
        (!dateTo || logDate <= toDate) &&
        (!urlFilter ||
          log.main_url.toLowerCase().includes(urlFilter.toLowerCase())) &&
        (!statusFilter || log.status === statusFilter)
      );
    });
    console.log(filteredLogs);
  }

  async function fetchLogs(user_id: string) {
    try {
      const response = await new Promise<any>((resolve, reject) => {
        fastapi(
          "GET",
          `/api/history/${user_id}`,
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
          `/api/history/${getId()}/${history_id}`,
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

<div class="flex w-full h-full bg-gray-50">
  <div class="w-full p-6">
    <div class="flex items-center mb-6">
      <div
        class="w-full bg-white shadow-md rounded-lg p-1.5 pl-2 flex items-center space-x-4 4xl:p-3 select-none"
      >
        <p class="4xl:text-lg">From</p>
        <input
          type="date"
          bind:value={dateFrom}
          on:change={filterLogs}
          class="rounded px-1 py-2 text-sm shadow-sm border-none 4xl:text-lg focus:ring-gray-500"
          placeholder="From Date"
        />
        <p class="4xl:text-lg">To</p>
        <input
          type="date"
          bind:value={dateTo}
          on:change={filterLogs}
          class="border rounded px-1 py-2 text-sm shadow-sm border-none 4xl:text-lg focus:ring-gray-500"
          placeholder="To Date"
        />
        <select
          bind:value={statusFilter}
          on:change={filterLogs}
          class="border rounded px-3 py-2 text-sm shadow-sm 4xl:text-lg focus:ring-gray-500"
        >
          <option value="">All Statuses</option>
          <option value="Test Completed">Test Completed</option>
          <option value="Test Canceled">Test Canceled</option>
        </select>
          <input
            type="text"
            placeholder="URL"
            bind:value={urlFilter}
            on:input={filterLogs}
            class="border rounded px-3 py-2 text-sm shadow-sm w-1/3 4xl:text-lg focus:ring-gray-500"
          />
      </div>
    </div>
    <Table shadow>
      <TableHead class="text-center text-sm 4xl:text-lg select-none">
        <TableHeadCell>DATE</TableHeadCell>
        <TableHeadCell>URL</TableHeadCell>
        <TableHeadCell>STATUS</TableHeadCell>
        <TableHeadCell>REPORT</TableHeadCell>
        <TableHeadCell>ACTION</TableHeadCell>
      </TableHead>
      <TableBody tableBodyClass="divide-y">
        {#each filteredLogs as log}
          <TableBodyRow class="text-center 4xl:text-lg">
            <TableBodyCell>{formatDate(log.time)}</TableBodyCell>
            <TableBodyCell>{log.main_url}</TableBodyCell>
            <TableBodyCell
              class={`select-none ${log.status === "Test Completed" ? "text-green-500" : "text-red-500"}`}
            >
              {log.status}
            </TableBodyCell>
            <TableBodyCell>
              <button
                on:click={() => downloadReport(log)}
                class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 disabled:bg-gray-500 disabled:cursor-not-allowed select-none"
                disabled={log.file === null}
              >
                Download
              </button>
            </TableBodyCell>
            <TableBodyCell>
              <button
                class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700 select-none"
                on:click={() => deleteLog(log._id)}
              >
                Delete
              </button>
            </TableBodyCell>
          </TableBodyRow>
        {/each}
      </TableBody>
    </Table>
  </div>
</div>
