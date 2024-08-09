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
  import { writable } from "svelte/store";
  import fastapi from "$lib/fastapi";
  import SignUp from "$lib/components/SignUp.svelte";
  import { getId } from "$lib/store";

  type User = {
    id: string;
    role: string;
    authorizer: string;
    created_at: string;
  };

  let users: User[] = [];
  let searchQuery: string = "";
  let filterRole: string = "all";
  let showCreateUser = writable(false);

  function closeModal() {
    showCreateUser.set(false);
    fetchUsers();
  }

  const handleSearch = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target) {
      searchQuery = target.value;
    }
  };

  const handleFilterRole = (event: Event) => {
    const target = event.target as HTMLSelectElement;
    if (target) {
      filterRole = target.value;
    }
  };

  async function handleLockUser(userId: string){
    if (userId === getId()){
      Swal.fire("Error!", "You can't lock yourself.", "error");
      return;
    }

    try {
        await lockUser(userId);
        users = users.filter((user) => user.id !== userId);
        Swal.fire("Locked!", "The user has been locked.", "success");
      } catch (error: any) {
        if (error.detail === "Unable to lock root administrator account.") {
          Swal.fire("Error!", `${error.detail}`, "error");
        } else {
          Swal.fire("Error!", "There was an error locking the user.", "error");
        }
      }
  }

  async function handleDeleteUser(userId: string) {
    const result = await Swal.fire({
      title: "Are you sure?",
      text: "This action is irreversible!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes",
      cancelButtonText: "No",
    });

    if (userId === getId()){
      Swal.fire("Error!", "You can't delete yourself.", "error");
      return;
    }

    if (result.isConfirmed) {
      try {
        await deleteUser(userId);
        users = users.filter((user) => user.id !== userId);
        Swal.fire("Deleted!", "The user has been deleted.", "success");
      } catch (error: any) {
        if (error.detail === "Unable to delete root administrator account.") {
          Swal.fire("Error!", `${error.detail}`, "error");
        } else {
          Swal.fire("Error!", "There was an error deleting the user.", "error");
        }
      }
    }
  }

  async function lockUser(userId: string) {
    return new Promise<void>((resolve, reject) => {
      fastapi("POST", `/user/${userId}/lock`, {}, resolve, reject);
    });
  }

  async function deleteUser(userId: string) {
    return new Promise<void>((resolve, reject) => {
      fastapi("DELETE", `/user/${userId}`, {}, resolve, reject);
    });
  }

  async function fetchUsers() {
    try {
      users = await new Promise((resolve, reject) => {
        fastapi("GET", "/user", {}, resolve, reject);
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

  $: filteredUsers = users.filter((user) => {
    const matchesQuery = user.id
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    const matchesRole = filterRole === "all" || user.role === filterRole;
    return matchesQuery && matchesRole;
  });
</script>

<section
  class="flex flex-col w-full items-center relative"
  style="height: 94vh;"
>
  <div class="h-full p-4 flex flex-col 4xl:p-6" style="width: 95%">
    <h1 class="text-2xl font-bold mb-3 4xl:text-4xl 4xl:mb-6 select-none">
      User Management
    </h1>
    <div
      class="flex justify-between items-center w-full bg-white max-h-16 rounded-lg mb-2 shadow-lg"
      style="height: 9%;"
    >
      <div
        class="flex items-center h-full justify-center items-center space-x-4 p-2"
      >
        <div class="relative 4xl:ml-1">
          <label for="table-search" class="sr-only">Search</label>
          <div
            class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none"
          >
            <svg
              class="w-4 h-4 text-gray-500"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 20"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
              />
            </svg>
          </div>
          <input
            type="text"
            id="table-search"
            on:input={handleSearch}
            class="block pt-2 ps-10 text-sm h-2/3 text-gray-900 border border-gray-300 rounded-lg w-80 bg-gray-50 focus:ring-blue-500 focus:border-blue-500 4xl:text-xl 4xl:w-96 select-none"
            placeholder="Search by username"
          />
        </div>
        <select
          on:change={handleFilterRole}
          class="text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 4xl:text-xl"
        >
          <option value="all">All Roles</option>
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <div class="flex items-center h-full justify-center p-3 4xl:mr-1">
        <button
          on:click={() => {
            $showCreateUser = true;
          }}
          class="px-2 py-1.5 4xl:px-3"
        >
          <svg
            class="w-6 h-6 text-gray-800 4xl:w-8 4xl:h-8"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              fill-rule="evenodd"
              d="M9 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4H7Zm8-1a1 1 0 0 1 1-1h1v-1a1 1 0 1 1 2 0v1h1a1 1 0 1 1 0 2h-1v1a1 1 0 1 1-2 0v-1h-1a1 1 0 0 1-1-1Z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>
    </div>
    <Table shadow>
      <TableHead class="text-center text-sm 4xl:text-lg select-none">
        <TableHeadCell>ID</TableHeadCell>
        <TableHeadCell>Role</TableHeadCell>
        <TableHeadCell>Authorizer</TableHeadCell>
        <TableHeadCell>Creation</TableHeadCell>
        <TableHeadCell>Actions</TableHeadCell>
      </TableHead>
      <TableBody tableBodyClass="divide-y select-none">
        {#each filteredUsers as user}
          <TableBodyRow class="text-center text-sm 4xl:text-lg">
            <TableBodyCell>{user.id}</TableBodyCell>
            <TableBodyCell>{user.role}</TableBodyCell>
            <TableBodyCell>{user.authorizer}</TableBodyCell>
            <TableBodyCell
              >{new Date(user.created_at).toLocaleString()}</TableBodyCell
            >
            <TableBodyCell>
              <button
                class="bg-yellow-400 text-white px-3 py-1 rounded hover:bg-yellow-600 hover:font-bold mr-4"
                on:click={() => handleLockUser(user.id)}
              >
                Lock
              </button>
              <button
                class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700 hover:font-bold"
                on:click={() => handleDeleteUser(user.id)}
              >
                Delete
              </button>
            </TableBodyCell>
          </TableBodyRow>
        {/each}
      </TableBody>
    </Table>
  </div>
  {#if $showCreateUser}
    <div
      class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-20"
    >
      <div
        class="min-h-96 overflow-auto bg-white rounded-lg shadow-lg"
        style="width: 33%; max-width:600px; height: 40%"
      >
        <SignUp onClose={closeModal} />
      </div>
    </div>
  {/if}
</section>
