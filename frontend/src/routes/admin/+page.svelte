<script lang="ts">
  import { onMount } from "svelte";
  import { mode, setMode } from "$lib/store";
  import SideBar from "$lib/components/SideBar.svelte";
  import UserManagement from "$lib/components/UserManagement.svelte";
  import LockManagement from "$lib/components/LockManagement.svelte";
  import CustomerInquiries from "$lib/components/CustomerInquiries.svelte";
  
  onMount(async () => {
    setMode("UserManagement");
  });

  $: current_mode = $mode;
</script>

<main class="w-screen h-screen flex flex-col bg-gray-100">
  <div class="flex flex-1 overflow-hidden h-full">
    <SideBar />
    <div class="flex-1 overflow-auto h-full">
      {#if current_mode === "UserManagement"}
        <UserManagement />
      {:else if current_mode === "LockManagement"}
        <LockManagement />
      {:else if current_mode === "CustomerInquiries"}
        <CustomerInquiries />
      {/if}
    </div>
  </div>
</main>
