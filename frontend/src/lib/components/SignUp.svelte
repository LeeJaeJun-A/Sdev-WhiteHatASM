<script lang="ts">
  import { onMount } from "svelte";
  import { getId } from "$lib/store";
  import { initializeSession } from "$lib/auth";
  import { get } from "svelte/store";
  import Swal from "sweetalert2";
  import fastapi from "$lib/fastapi";

  export let onClose;
  let user_id: string = "";
  let password: string = "";
  let role: string = "user";

  const handleRole = (event: Event) => {
    const target = event.target as HTMLSelectElement;
    if (target) {
      role = target.value;
    }
  };

  const handleSubmit = async (event: Event) => {
    event.preventDefault();

    const authorizer: string | null = getId();
    const userData = { id: user_id, password, role, authorizer };

    try {
      await new Promise((resolve, reject) => {
        fastapi("POST", "/api/user", userData, resolve, reject);
      });

      Swal.fire(
        "Success!",
        "The user has been created successfully.",
        "success"
      );
      onClose();
    } catch (error: any) {
      Swal.fire(
        "Error!",
        error.detail || "There was an error creating the user.",
        "error"
      );
    }
  };

  onMount(async () => {
    await initializeSession();
  });
</script>

<section
  class="bg-white rounded-lg p-8 flex flex-col justify-center items-center w-full h-full "
>
  <span class="text-2xl mb-3 4xl:text-3xl 4xl:mb-6 ">Create User</span>
  <div class="w-full">
    <form
      on:submit|preventDefault={handleSubmit}
      class="w-full flex flex-col space-y-4 4xl:space-y-8"
    >
      <div>
        <label for="id" class="block text-sm font-medium text-gray-700 4xl:text-xl"
          >ID</label
        >
        <input
          id="id"
          type="text"
          bind:value={user_id}
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 4xl:text-xl"
          required
        />
      </div>
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 4xl:text-xl"
          >Password</label
        >
        <input
          id="password"
          type="password"
          bind:value={password}
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 4xl:text-xl"
          required
        />
      </div>
      <div>
        <label for="role" class="block text-sm font-medium text-gray-700 4xl:text-xl"
          >Role</label
        >
        <select
          id="role"
          on:change={handleRole}
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 4xl:text-xl"
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <div class="flex pt-1 space-x-4 justify-center w-full">
        <button
          type="submit"
          class="w-1/6 px-10 py-2 flex justify-center items-center bg-blue-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 4xl:text-lg 4xl:px-12"
          >
          Create
        </button>
        <button
          type="button"
          on:click={onClose}
          class="px-10 py-2 w-1/6 flex justify-center items-center bg-gray-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 4xl:text-lg 4xl:px-12"
        >
          Close
        </button>
      </div>
    </form>
  </div>
</section>
