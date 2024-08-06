<script>
  import { goto } from "$app/navigation";
</script>

<nav
  class="flex justify-between items-center p-2 border-gray-200 bg-gray-50 max-h-20 4xl:p-4"
  style="height: 8%"
>
  <div class="flex items-center space-x-2 h-full">
    <img src="/shinnam.png" class="h-full" alt="logo" />
    <span class="text-xl font-semibold select-none 4xl:text-3xl">Shinnam</span>
  </div>
  <ul class="flex space-x-20 4xl:space-x-40">
    <li>
      <a href="/" class="hover:text-gray-400 4xl:text-2xl select-none">Home</a>
    </li>
    <li>
      <a href="/about" class="hover:text-gray-400 4xl:text-2xl select-none"
        >About</a
      >
    </li>
    <li>
      <a href="/contact" class="hover:text-gray-400 4xl:text-2xl select-none"
        >Contact</a
      >
    </li>
  </ul>
  <div>
    <button
      class="bg-blue-800 text-sm text-white rounded-full h-7 w-20 hover:bg-blue-900 4xl:text-xl 4xl:w-32 4xl:h-10 select-none"
      on:click={() => goto("/login")}
    >
      로그인
    </button>
  </div>
</nav>
