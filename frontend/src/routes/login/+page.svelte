<script lang="ts">
  import { type Writable, writable } from "svelte/store";
  import { goto } from "$app/navigation";
  import { EyeOutline, EyeSlashOutline } from "flowbite-svelte-icons";
  import Swal from "sweetalert2";
  import fastapi from "$lib/fastapi";
  import { setId } from "$lib/store";

  let id: Writable<string> = writable("");
  let password: string = "";
  let showPassword: boolean = false;

  async function handleLogin(event: Event) {
    event.preventDefault();
    if ($id && password) {
      const params = { id: $id, password: password };
      fastapi(
        "POST",
        "/api/token",
        params,
        (data) => {
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);

          Swal.fire({
            icon: "success",
            title: "Login Successful",
            timer: 1000,
            showConfirmButton: false,
          }).then(() => {
            if (data.role === "admin") {
              setId($id);
              goto("/admin", { replaceState: true });
            } else {
              setId($id);
              goto("/user", { replaceState: true });
            }
          });
        },
        (error) => {
          if (
            error.detail === "User not found" ||
            error.detail === "Invalid Access"
          ) {
            Swal.fire({
              icon: "error",
              title: "Login Failed",
              text: `${error.detail}. Please check your account.`,
            });
            return;
          }

          if (error.remaining_attempts === 0) {
            if (error.detail === "Incorrect ID or password") {
              Swal.fire({
                icon: "error",
                title: "Login Failed",
                text: `${error.detail}. This account is locked.`,
              });
              return;
            }
            Swal.fire({
              icon: "error",
              title: "Login Failed",
              text: `${error.detail}`,
            });
            return;
          }

          Swal.fire({
            icon: "error",
            title: "Login Failed",
            text: `${error.detail} (Remaining attempts: ${error.remaining_attempts})`,
          });
        }
      );
    }
  }

  function togglePasswordVisibility() {
    showPassword = !showPassword;
  }

  function handlePassword(event: Event) {
    const target = event.target as HTMLInputElement;
    password = target?.value || "";
  }
</script>

<main class="bg-white w-screen h-screen">
  <head
    class="flex justify-center items-center p-2 border-gray-200 bg-gray-50 max-h-20 4xl:p-4"
    style="height: 8%"
  >
    <button
      class="flex items-center space-x-2 h-full select-none"
      on:click={() => goto("/")}
    >
      <img src="/shinnam.png" class="h-full" alt="logo" />
      <span class="text-xl font-semibold select-none 4xl:text-3xl">Shinnam</span
      >
    </button>
  </head>
  <div class="w-full flex" style="height: 92%;">
    <div class="w-1/2 h-full flex justify-center items-center select-none">
      <div
        class="w-full h-2/3 p-20 space-y-8 flex flex-col justify-center 4xl:space-y-24 4xl:p-52"
      >
        <div
          class="w-full flex items-center space-x-2 4xl:space-x-5"
          style="height: 15%;"
        >
          <img src="/shinnam.png" class="h-full" alt="logo" />
          <span class="text-2xl font-semibold select-none 4xl:text-7xl"
            >AI 활용 화이트햇 ASM</span
          >
        </div>
        <div class="flex space-x-2 fade-in delay-500">
          <svg
            class="w-6 h-6 text-blue-700 4xl:w-10 4xl:h-10"
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
              d="M8.5 11.5 11 14l4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
            />
          </svg>
          <div class="flex flex-col">
            <p class="mb-1 font-semibold 4xl:text-4xl">
              한 번의 URL 입력으로 손쉽게 시작하는 보안 점검
            </p>
            <p class="text-sm text-gray-500 4xl:text-2xl">
              간단히 웹사이트의 URL을 입력하면 관리 환경에 접속할 수 있습니다.
            </p>
            <p class="text-sm text-gray-500 4xl:text-2xl">
              간편하게 웹사이트를 등록하고 관리하세요.
            </p>
          </div>
        </div>
        <div class="flex space-x-2 fade-in delay-1000">
          <svg
            class="w-6 h-6 text-blue-700 4xl:w-10 4xl:h-10"
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
              d="M8.5 11.5 11 14l4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
            />
          </svg>
          <div class="flex flex-col">
            <p class="mb-1 font-semibold 4xl:text-4xl">
              맞춤형 보안 점검 선택이 가능한 웹사이트 관리
            </p>
            <p class="text-sm text-gray-500 4xl:text-2xl">
              웹사이트의 특성에 맞춰 다양한 취약점 점검 옵션을 선택할 수
              있습니다.
            </p>
            <p class="text-sm text-gray-500 4xl:text-2xl">
              필요한 점검을 선택하여 최적의 보안 상태를 유지하세요.
            </p>
          </div>
        </div>
        <div class="flex space-x-2 fade-in delay-1500">
          <svg
            class="w-6 h-6 text-blue-700 4xl:w-10 4xl:h-10"
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
              d="M8.5 11.5 11 14l4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
            />
          </svg>
          <div class="flex flex-col">
            <p class="mb-1 font-semibold 4xl:text-4xl">
              AI 기반의 자동화된 취약점 점검 보고서
            </p>
            <p class="text-sm text-gray-500 4xl:text-2xl">
              AI를 활용하여 선택한 취약점 점검을 자동화하고, 상세한 보고서를
              제공합니다.
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="w-1/2 h-full flex justify-center items-center">
      <form
        class="w-3/4 h-2/3 rounded-xl shadow-lg border flex flex-col items-center justify-center space-y-10 4xl:space-y-20"
        on:submit|preventDefault={handleLogin}
      >
        <div class="w-5/6">
          <label
            for="id"
            class="block mb-2 text-sm font-medium text-gray-900 4xl:text-2xl 4xl:mb-4"
            >ID</label
          >
          <input
            type="text"
            name="id"
            id="id"
            class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 4xl:text-2xl 4xl:p-4 4xl:mb-4"
            placeholder="아이디를 입력하세요"
            bind:value={$id}
            autocomplete="username"
            required
          />
        </div>
        <div class="w-5/6">
          <div
            class="flex items-center justify-between mb-2 text-sm 4xl:mb-4 4xl:text-2xl"
          >
            <label for="password" class="font-medium text-gray-900"
              >비밀번호</label
            >
            <div>
              <a
                href="/contact"
                class="font-semibold text-indigo-600 hover:text-indigo-500"
                >비밀번호를 잊어버리셨나요?</a
              >
            </div>
          </div>
          <div class="relative">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              id="password"
              placeholder="••••••••"
              class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 4xl:text-2xl 4xl:p-4 4xl:mb-8"
              required
              autocomplete="current-password"
              on:input={handlePassword}
            />
            <button
              type="button"
              class="absolute inset-y-0 right-3 flex items-center text-sm 4xl:text-xl"
              on:click={togglePasswordVisibility}
            >
              {#if showPassword}
                <EyeOutline
                  class="h-5 w-5 text-gray-500 4xl:h-8 4xl:w-8"
                  aria-hidden="true"
                />
              {:else}
                <EyeSlashOutline
                  class="h-5 w-5 text-gray-500  4xl:h-8 4xl:w-8"
                  aria-hidden="true"
                />
              {/if}
            </button>
          </div>
        </div>
        <button
          type="submit"
          class="w-5/6 text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center 4xl:text-2xl 4xl:px-8 4xl:py-4"
          >로그인</button
        >
      </form>
    </div>
  </div>
</main>

<style>
  @keyframes fadeIn {
    0% {
      opacity: 0;
      transform: scale(0.9);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }

  .fade-in {
    opacity: 0;
    animation: fadeIn 1.5s ease-out forwards;
  }

  .delay-500 {
    animation-delay: 0.5s;
  }

  .delay-1000 {
    animation-delay: 1s;
  }

  .delay-1500 {
    animation-delay: 1.5s;
  }
</style>
