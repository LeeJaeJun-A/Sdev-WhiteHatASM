<script lang="ts">
  import NavBar from "$lib/components/NavBar.svelte";

  interface FAQ {
    question: string;
    answer: string;
  }

  let FAQs: FAQ[] = [
    { question: "이 웹사이트의 주요 기능은 무엇인가요?", answer: "이 웹사이트는 입력한 URL을 크롤링하여 가능한 CVE 테스트 목록을 보여주고, 선택한 CVE를 통해 보안 테스트를 진행한 후 AI를 사용하여 자동으로 보고서를 생성해주는 서비스입니다." },
    { question: "CVE란 무엇인가요?", answer: "CVE(Common Vulnerabilities and Exposures)는 알려진 보안 취약점의 표준화된 목록으로, 웹사이트나 소프트웨어의 보안 취약점을 식별하고 관리하는 데 사용됩니다." },
    { question: "모든 웹사이트에 대해 보안 테스트를 할 수 있나요?", answer: "아니요, 본인 관리 하의 웹사이트만 검사할 수 있습니다. 이외의 웹사이트에 대한 검사는 법적 처벌을 받을 수 있습니다." },
    { question: "AI 보고서는 어떤 내용을 포함하나요?", answer: "AI 보고서는 선택한 CVE를 기반으로 한 보안 테스트 결과, 발견된 취약점의 상세 설명, 그리고 이에 따른 보안 개선 권장 사항을 포함합니다." },
    { question: "웹사이트 크롤링은 어떻게 이루어지나요?", answer: "사용자가 입력한 URL을 기반으로 자동화된 크롤링을 통해 서버 도메인과 소프트웨어 버전을 탐지하고, 이에 따라 적용 가능한 CVE 목록을 생성합니다." },
    { question: "CVE 테스트는 어떻게 진행되나요?", answer: "사용자가 원하는 CVE를 선택하면, 해당 취약점에 대해 자동화된 시뮬레이션 테스트가 수행되며, 그 결과를 바탕으로 AI 보고서가 생성됩니다." },
    { question: "CVE 목록은 어떻게 업데이트되나요?", answer: "CVE 목록은 최신 보안 데이터베이스를 기반으로 자동 업데이트되며, 새로운 취약점이 발견될 때마다 목록에 추가됩니다." },
    { question: "계정을 생성하고 싶습니다. 어떻게 해야 하나요?", answer: "계정을 생성하려면 Contact 페이지를 통해 문의해주시면 됩니다." },
    { question: "보고서의 내용을 외부로 공유해도 되나요?", answer: "보고서의 내용은 사용자가 관리하는 웹사이트의 보안 개선을 위해 사용할 수 있으며, 외부 공유 시에는 법적 문제를 고려해야 합니다." }
  ];
  
  let expanded: number | null = null;

  function toggleDetail(index: number) {
    expanded = expanded === index ? null : index;
  }
</script>

<div class="bg-white w-screen h-screen">
  <NavBar />
  <div
    class="w-full h-full flex items-center justify-center flex-col overflow-auto"
    style="height: 92%;"
  >
    <div class="w-full h-full flex justify-center items-center">
      <table class="w-5/6 border border-gray-300 rounded-lg shadow-lg">
        <tbody>
          {#each FAQs as faq, index}
            <tr class="cursor-pointer hover:bg-gray-50 transition-colors" on:click={() => toggleDetail(index)}>
              <td class="border-b border-gray-300 p-3 text-gray-700 font-semibold">{faq.question}</td>
            </tr>
            {#if expanded == index}
              <tr>
                <td class="p-3 bg-gray-100 text-gray-600">{faq.answer}</td>
              </tr>
            {/if}
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>
