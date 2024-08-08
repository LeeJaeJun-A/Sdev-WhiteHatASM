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

  interface LogEntry {
    date: string;
    url: string;
    status: string;
  }

  // Mock data for demonstration
  let logs : LogEntry[] = [
    {
      date: "2024-08-01",
      url: "https://www.naver.com",
      status: "Completed",
    },
    {
      date: "2024-08-02",
      url: "https://www.google.com",
      status: "Stopped",
    },
    {
      date: "2024-08-02",
      url: "https://www.shinnam12324.com",
      status: "Failed to crawl",
    },
    // Add more sample data here
  ];

  let filteredLogs: LogEntry[] = [...logs];
  let dateFilter: string = "";
  let urlFilter: string = "";
  let statusFilter: string = "";

  function downloadReport(log : LogEntry) {
    console.log(getId());
    console.log(log.date);
    console.log(log.url);
  }

  function filterLogs() {
    filteredLogs = logs.filter((log) => {
      return (
        (!dateFilter || log.date.includes(dateFilter)) &&
        (!urlFilter ||
          log.url.toLowerCase().includes(urlFilter.toLowerCase())) &&
        (!statusFilter ||
          log.status.toLowerCase().includes(statusFilter.toLowerCase()))
      );
    });
  }
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
          <TableBodyRow class="text-center">
            <TableBodyCell>{log.date}</TableBodyCell>
            <TableBodyCell>{log.url}</TableBodyCell>
            <TableBodyCell>{log.status}</TableBodyCell>
            <TableBodyCell
              ><button on:click={() => downloadReport(log)} class="text-blue-700">Download</button
              ></TableBodyCell
            >
            <TableBodyCell
              ><button class="text-red-500">Delete</button
              ></TableBodyCell
            >
          </TableBodyRow>
        {/each}
      </TableBody>
    </Table>
  </div>
</div>
