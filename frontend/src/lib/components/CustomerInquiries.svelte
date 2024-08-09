<script lang="ts">
  import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
  } from "flowbite-svelte";
  import Swal from "sweetalert2";
  import fastapi from "$lib/fastapi";
  import { onMount } from "svelte";

  interface Inquiry {
    _id: string;
    title: string;
    email: string;
    phone: string;
    message: string;
    is_read: boolean;
  }

  let inquiries: Inquiry[] = [];

  let expandedId: number | null = null;

  async function toggleDetail(index: number, id: string): Promise<void> {
    expandedId = expandedId === index ? null : index;
    console.log(id);
    try {
      await new Promise<void>((resolve, reject) => {
        fastapi("PUT", "/contact/read", { id }, resolve, reject);
      });
    } catch (error) {
      console.error("Error update inquiry status:", error);
    }
  }

  async function deleteInquiry(id: string, event: MouseEvent): Promise<void> {
    event.stopPropagation();

    try {
      await new Promise<void>((resolve, reject) => {
        fastapi("DELETE", "/contact", { id }, resolve, reject);
      });
      inquiries = inquiries.filter((inquiry) => inquiry._id !== id);
    } catch (error) {
      console.error("Error deleting inquiry:", error);
    }
  }

  async function fetchInquiries() {
    try {
      inquiries = await new Promise((resolve, reject) => {
        fastapi("GET", "/contact", {}, resolve, reject);
      });

      console.log(inquiries);
    } catch (error) {
      let errorMessage = "An unknown error occurred";
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      Swal.fire({
        icon: "error",
        title: "Error",
        text: errorMessage,
      });
    }
  }

  onMount(fetchInquiries);
</script>

<section
  class="flex flex-col w-full items-center relative"
  style="height: 94vh;"
>
  <div class="h-full p-4 flex flex-col 4xl:p-6" style="width: 95%">
    <h1 class="text-2xl font-bold mb-3 4xl:text-4xl 4xl:mb-6 select-none">
      Customer Inquiries
    </h1>
    <Table shadow>
      <TableHead class="text-center text-sm 4xl:text-lg select-none">
        <TableHeadCell>Title</TableHeadCell>
        <TableHeadCell>Email</TableHeadCell>
        <TableHeadCell>Phone</TableHeadCell>
        <TableHeadCell>Actions</TableHeadCell>
      </TableHead>
      <TableBody tableBodyClass="divide-y select-none">
        {#each inquiries as inquiry, index}
          <TableBodyRow
            class={`cursor-pointer text-center text-sm 4xl:text-lg ${expandedId === index ? "bg-gray-200" : "hover:bg-gray-50"}`}
            on:click={() => toggleDetail(index, inquiry._id)}
          >
            <TableBodyCell>{inquiry.title}</TableBodyCell>
            <TableBodyCell>{inquiry.email}</TableBodyCell>
            <TableBodyCell>{inquiry.phone}</TableBodyCell>
            <TableBodyCell>
              <button
                class="bg-red-500 text-white px-3 py-1 rounded"
                on:click={(e) => deleteInquiry(inquiry._id, e)}
              >
                Delete
              </button>
            </TableBodyCell>
          </TableBodyRow>
          {#if expandedId === index}
            <TableBodyRow class="bg-gray-50">
              <TableBodyCell colspan="4" class="p-4">
                {inquiry.message}
              </TableBodyCell>
            </TableBodyRow>
          {/if}
        {/each}
      </TableBody>
    </Table>
  </div>
</section>
