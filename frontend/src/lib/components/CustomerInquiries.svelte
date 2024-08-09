<script lang="ts">
  import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
  } from "flowbite-svelte";

  interface Inquiry {
    id: number;
    title: string;
    email: string;
    phone: string;
    message: string;
  }

  // 샘플 데이터 (실제 데이터는 API 등을 통해 받아올 수 있음)
  let inquiries: Inquiry[] = [
    {
      id: 1,
      title: "문의 제목 1",
      email: "user1@example.com",
      phone: "123-456-7890",
      message: "세부 메시지 내용 1",
    },
    {
      id: 2,
      title: "문의 제목 2",
      email: "user2@example.com",
      phone: "987-654-3210",
      message: "세부 메시지 내용 2",
    },
  ];

  let expandedId: number | null = null;

  function toggleDetail(id: number): void {
    expandedId = expandedId === id ? null : id;
  }

  function deleteInquiry(id: number, event: MouseEvent): void {
    event.stopPropagation(); // 클릭 이벤트 전파 방지
    inquiries = inquiries.filter((inquiry) => inquiry.id !== id);
  }
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
        {#each inquiries as inquiry}
          <TableBodyRow
            class={`cursor-pointer text-center text-sm 4xl:text-lg ${expandedId === inquiry.id ? "bg-gray-200" : "hover:bg-gray-50"}`}
            on:click={() => toggleDetail(inquiry.id)}
          >
            <TableBodyCell>{inquiry.title}</TableBodyCell>
            <TableBodyCell>{inquiry.email}</TableBodyCell>
            <TableBodyCell>{inquiry.phone}</TableBodyCell>
            <TableBodyCell>
              <button
                class="bg-red-500 text-white px-3 py-1 rounded"
                on:click={(e) => deleteInquiry(inquiry.id, e)}
              >
                Delete
              </button>
            </TableBodyCell>
          </TableBodyRow>
          {#if expandedId === inquiry.id}
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
