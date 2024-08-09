<script lang="ts">
  import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
  } from "flowbite-svelte";
  import { onMount } from "svelte";
  import Swal from "sweetalert2";
  import fastapi from "$lib/fastapi";

  type User = {
    id: string;
    role: string;
    authorizer: string;
    locked_at: string;
  };

  let locked_users: User[] = [];

  async function unlockUser(userId: string) {
    try {
      await new Promise<void>((resolve, reject) => {
        fastapi("POST", `/user/${userId}/unlock`, {}, resolve, reject);
      });

      locked_users = locked_users.filter((user) => user.id !== userId);
      Swal.fire("Unlocked!", "The user has been unlocked.", "success");
    } catch {
      Swal.fire("Error!", "There was an error unlock the user.", "error");
    }
  }

  async function fetchUsers() {
    try {
      locked_users = await new Promise((resolve, reject) => {
        fastapi("GET", "/user/locked", {}, resolve, reject);
      });
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

  onMount(fetchUsers);
</script>

<section
  class="flex flex-col w-full items-center relative"
  style="height: 94vh;"
>
  <div class="h-full p-4 4xl:p-6" style="width: 95%">
    <h1 class="text-2xl font-bold mb-3 4xl:text-4xl 4xl:mb-6 select-none">
      Lock Management
    </h1>
    <Table shadow>
      <TableHead class="text-center text-sm 4xl:text-lg select-none">
        <TableHeadCell>ID</TableHeadCell>
        <TableHeadCell>Role</TableHeadCell>
        <TableHeadCell>Authorizer</TableHeadCell>
        <TableHeadCell>Locked At</TableHeadCell>
        <TableHeadCell>Actions</TableHeadCell>
      </TableHead>
      <TableBody tableBodyClass="divide-y select-none">
        {#each locked_users as user}
          <TableBodyRow class="text-center text-sm 4xl:text-lg">
            <TableBodyCell>{user.id}</TableBodyCell>
            <TableBodyCell>{user.role}</TableBodyCell>
            <TableBodyCell>{user.authorizer}</TableBodyCell>
            <TableBodyCell
              >{new Date(user.locked_at).toLocaleString()}</TableBodyCell
            >
            <TableBodyCell>
              <button
                class="text-sm bg-red-400 text-white px-3 py-1 rounded hover:text-yellow-600 hover:font-bold 4xl:text-lg"
                on:click={() => unlockUser(user.id)}
              >
                Unlock
              </button>
            </TableBodyCell>
          </TableBodyRow>
        {/each}
      </TableBody>
    </Table>
  </div>
</section>
