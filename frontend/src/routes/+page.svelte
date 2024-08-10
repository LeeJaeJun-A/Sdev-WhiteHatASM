<script lang="ts">
  import { goto } from "$app/navigation";
  import NavBar from "$lib/components/NavBar.svelte";
</script>

<main class="bg-white w-screen h-screen">
  <NavBar />
  <div class="relative w-full flex justify-center" style="height: 92%;">
    <img
      src="/preview.png"
      alt="preview"
      class="absolute right-10 w-3/5 z-1 opacity-70 4xl:right-40"
      style="bottom: 20%;"
    />
    <div class="w-5/6 flex flex-col justify-center h-5/6 z-10 space-y-2 select-none">
      <p class="text-6xl font-bold fade-in delay-500 4xl:text-8xl">AI 활용 화이트햇</p>
      <p class="text-6xl font-bold text-blue-800 fade-in delay-500  4xl:text-8xl">ASM</p>
      <p class="text-lg fade-in delay-1000 4xl:text-2xl">"자동화된 보안 검토로 시간과 인력을 절약하고</p>
      <p class="text-lg pb-5 fade-in delay-1000 4xl:text-2xl 4xl:pb-10">서브 도메인과 CVE 취약점에 효과적으로 대응하세요."</p>
      <button class="w-32 h-10 border bg-gray-50 rounded-full shadow-md fade-in delay-1500 4xl:text-2xl 4xl:w-52 4xl:h-16"
      on:click={()=>goto("/FAQ")}
      >
        Learn More
      </button>
    </div>
  </div>
</main>

<style>
  @keyframes fadeIn {
    from {
      opacity: 0;
      visibility: hidden;
    }
    to {
      opacity: 1;
      visibility: visible;
    }
  }

  .fade-in {
    opacity: 0;
    visibility: hidden;
    animation: fadeIn 1s ease-in-out forwards;
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
