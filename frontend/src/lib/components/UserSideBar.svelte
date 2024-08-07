<script lang="ts">
  import {
    Sidebar,
    SidebarWrapper,
    SidebarItem,
    SidebarGroup,
  } from "flowbite-svelte";
  import { initializeSession, logout } from "$lib/auth";
  import { ChartPieSolid } from "flowbite-svelte-icons";
  import { onMount } from "svelte";
  import { writable, type Writable } from "svelte/store";
  import { setUserMode } from "$lib/store";

  let showSideBar: Writable<boolean> = writable(true);

  async function clickHome() {
    await initializeSession();
    setUserMode("home");
  }

  async function clickHistory() {
    await initializeSession();
    setUserMode("history");
  }

  function clickLogout() {
    logout();
  }

  function toggleSideBar() {
    showSideBar.update((value) => !value);
  }

  onMount(async () => {
    await initializeSession();
    showSideBar.set(false);
  });
</script>

{#if $showSideBar}
  <div class="h-full min-w-64 select-none" style="width: 20%;">
    <Sidebar class="w-full h-full">
      <SidebarWrapper class="w-full h-full bg-gray-200 border">
        <SidebarGroup class="w-full h-full 4xl:space-y-5 4xl:p-3">
          <div class="flex justify-between w-full" style="height: 5%;">
            <div class="flex truncate items-center space-x-2">
              <img src="/shinnam.png" alt="logo" class="h-full" />
              <p class="4xl:text-3xl">ID</p>
            </div>
            <button on:click={toggleSideBar}>
              <svg
                class="w-6 h-6 text-gray-500 4xl:w-10 4xl:h-10"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="m15 19-7-7 7-7"
                />
              </svg>
            </button>
          </div>
          <SidebarItem label="Home" class="4xl:text-3xl" on:click={clickHome}>
            <svelte:fragment slot="icon">
              <svg
                class="w-6 h-6 text-gray-500 group-hover:text-gray-900 4xl:w-10 4xl:h-10"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  fill-rule="evenodd"
                  d="M11.293 3.293a1 1 0 0 1 1.414 0l6 6 2 2a1 1 0 0 1-1.414 1.414L19 12.414V19a2 2 0 0 1-2 2h-3a1 1 0 0 1-1-1v-3h-2v3a1 1 0 0 1-1 1H7a2 2 0 0 1-2-2v-6.586l-.293.293a1 1 0 0 1-1.414-1.414l2-2 6-6Z"
                  clip-rule="evenodd"
                />
              </svg>
            </svelte:fragment>
          </SidebarItem>
          <SidebarItem
            label="History"
            class="4xl:text-3xl"
            on:click={clickHistory}
          >
            <svelte:fragment slot="icon">
              <ChartPieSolid
                class="w-6 h-6 text-gray-500 group-hover:text-gray-900 4xl:w-10 4xl:h-10"
              />
            </svelte:fragment>
          </SidebarItem>
          <SidebarItem
            label="Logout"
            class="4xl:text-3xl"
            on:click={clickLogout}
          >
            <svelte:fragment slot="icon">
              <svg
                class="w-6 h-6 text-gray-500 group-hover:text-gray-900 4xl:w-10 4xl:h-10"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 12H8m12 0-4 4m4-4-4-4M9 4H7a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h2"
                />
              </svg>
            </svelte:fragment>
          </SidebarItem>
        </SidebarGroup>
      </SidebarWrapper>
    </Sidebar>
  </div>
{:else}
  <div class="h-full select-none max-w-20" style="width: 4%;">
    <Sidebar class="w-full h-full">
      <SidebarWrapper class="w-full h-full bg-gray-200 border">
        <SidebarGroup
          class="w-full h-full flex flex-col items-center space-y-4 4xl:space-y-7 4xl:p-3"
        >
          <button on:click={toggleSideBar}>
            <svg
              class="w-6 h-6 text-gray-500 4xl:w-10 4xl:h-10"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m10 16 7-7-7-7"
              />
            </svg>
          </button>
          <button on:click={clickHome}>
            <svg
              class="w-6 h-6 text-gray-500 group-hover:text-gray-900 4xl:w-10 4xl:h-10"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                fill-rule="evenodd"
                d="M11.293 3.293a1 1 0 0 1 1.414 0l6 6 2 2a1 1 0 0 1-1.414 1.414L19 12.414V19a2 2 0 0 1-2 2h-3a1 1 0 0 1-1-1v-3h-2v3a1 1 0 0 1-1 1H7a2 2 0 0 1-2-2v-6.586l-.293.293a1 1 0 0 1-1.414-1.414l2-2 6-6Z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
          <button on:click={clickHistory}
            ><ChartPieSolid
              class="w-6 h-6 text-gray-500 group-hover:text-gray-900 4xl:w-10 4xl:h-10"
            /></button
          >
          <button on:click={clickLogout}
            ><svg
              class="w-6 h-6 text-gray-500 group-hover:text-gray-900 4xl:w-10 4xl:h-10"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20 12H8m12 0-4 4m4-4-4-4M9 4H7a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h2"
              /></svg
            ></button
          >
        </SidebarGroup>
      </SidebarWrapper>
    </Sidebar>
  </div>
{/if}
