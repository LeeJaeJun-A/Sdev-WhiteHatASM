<script lang="ts">
  import { onMount } from "svelte";
  import { userMode, setUserMode } from "$lib/store";
  import UserHome from "$lib/components/UserHome.svelte";
  import UserHistory from "$lib/components/UserHistory.svelte";
  import UserSideBar from "$lib/components/UserSideBar.svelte";
  onMount(async () => {
    setUserMode("home");
  });

  $: current_mode = $userMode;
</script>

<main class="flex w-screen h-screen">
  <UserSideBar />
  <div class="flex-grow">
    <div class="h-screen flex flex-col">
      <div class="flex-1 overflow-auto h-full">
        {#if current_mode === "home"}
          <UserHome />
        {:else if current_mode === "history"}
          <UserHistory />
        {/if}
      </div>
    </div>
  </div>
</main>
