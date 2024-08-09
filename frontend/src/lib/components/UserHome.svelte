<script lang="ts">
  import { writable } from "svelte/store";
  import { currentUrl, getCurrentUrl, getId, setCurrentUrl, setHistoryID } from "$lib/store";
  import { goto } from "$app/navigation";
  import Swal from "sweetalert2";
  import fastapi from "$lib/fastapi";
  import { onMount } from "svelte";

  let urls : string[] = [];

  let agreedToTerms = writable(false);

  function handleCheck() {
    agreedToTerms.update((value) => !value);
  }

  async function fetchURLs(){
    try {
      const response = await new Promise<any>((resolve, reject) => {
        fastapi(
          "GET",
          `/history/${getId()}/recent`,
          {},
          (data) => resolve(data),
          (error) => reject(error)
        );
      });

      urls = response;
    } catch (err) {
      console.error("Error getting history: ", err);
    }
  }

  async function startInspection() {
    const url = getCurrentUrl();

    if (!url) {
      Swal.fire({
        icon: "error",
        title: "Invalid URL",
        text: `URL을 입력해주세요.`,
      });
      return;
    }

    if (!/^https?:\/\//i.test(url)) {
      Swal.fire({
        icon: "error",
        title: "Invalid URL",
        text: "URL에 http:// 또는 https://를 포함해야 합니다.",
      });
      return;
    }

    try {
      const validationResponse = await new Promise<{ valid: boolean }>(
        (resolve, reject) => {
          fastapi("POST", "/validate-url", { url }, resolve, reject);
        }
      );

      if (validationResponse.valid === false) {
        Swal.fire({
          icon: "error",
          title: "Invalid URL",
          text: "유효하지 않은 URL 입니다.",
        });
        return;
      }
      goto("/loading");
      
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: `${error}`,
      });
    }
  }

  onMount(() => {
    setCurrentUrl("");
    fetchURLs();
  });
</script>

<div class="flex w-full h-full select-none">
  <div class="w-full h-full">
    <div class="flex items-center bg-gray-50 shadow-md h-full rounded-lg p-6">
      <div class="w-1/2 h-full flex flex-col items-center">
        <div
          class="w-11/12 h-full bg-white shadow-lg rounded-lg py-2 px-3 overflow-auto flex flex-col items-center"
        >
          <p
            class="w-full text-xl flex justify-center items-center font-bold text-center mb-2 4xl:text-3xl"
          >
            최근 URL
          </p>
          {#each urls as url}
            <button
              class="hover:bg-gray-100 w-5/6 py-2 border-b border-gray-300 4xl:text-2xl truncate"
              on:click={() => setCurrentUrl(url)}>{url}</button
            >
          {/each}
        </div>
      </div>
      <div class="w-1/2 h-full flex justify-center items-center">
        <div
          class="w-11/12 h-full border bg-white flex flex-col justify-center items-center rounded-lg shadow-md"
        >
          <p
            class="text-left w-5/6 text-lg font-semibold 4xl:text-3xl 4xl:mb-2"
          >
            URL
          </p>
          <div class="w-full flex justify-center items-center mb-8 4xl:mb-20">
            <input
              bind:value={$currentUrl}
              type="text"
              placeholder="ex) https://www.shinnam.com"
              class="p-2 border border-gray-300 rounded w-5/6 4xl:text-2xl focus:border-gray-400 focus:border-2 outline-none focus:ring-0"
            />
          </div>
          <p
            class="text-left w-5/6 text-lg font-semibold 4xl:text-3xl 4xl:mb-2"
          >
            이용약관
          </p>
          <div
            class="w-5/6 h-1/2 border overflow-auto text-sm rounded-lg bg-gray-50 4xl:text-base"
          >
            <p>
              본 약관은 웹 취약점 공격을 시뮬레이션하는 사이트(이하 "서비스")의
              이용 조건과 관련한 내용을 규정합니다. 서비스에 접근하고
              이용함으로써, 사용자는 본 약관에 동의하는 것으로 간주됩니다.
            </p>
            <br />
            <p class="font-semibold">1. 서비스 이용 자격</p>
            <p>
              1.1 서비스는 해당 웹 사이트의 담당자 및 합법적인 보안 평가를
              목적으로 하는 사용자만 이용할 수 있습니다.
            </p>
            <p>
              1.2 악의적인 목적이나 불법적인 행위를 위해 서비스를 이용하는 것은
              엄격히 금지됩니다.
            </p>
            <br />
            <p class="font-semibold">2. 사용자의 책임</p>
            <p>2.1 사용자는 본 서비스의 이용에 따른 모든 책임을 집니다.</p>
            <p>
              2.2 서비스 이용 과정에서 발생하는 모든 행위는 사용자의 책임 하에
              있으며, 이는 법적 처벌의 대상이 될 수 있습니다.
            </p>
            <br />
            <p class="font-semibold">3. 정보 수집 및 이용</p>
            <p>
              3.1 본 서비스는 웹 크롤링 등의 기술을 통해 정보를 수집할 수
              있습니다.
            </p>
            <p>
              3.2 수집된 정보는 서비스 제공 및 품질 향상을 위한 목적으로만
              사용되며, 사용자의 동의 없이 제3자에게 제공되지 않습니다.
            </p>
            <p>
              3.3 분석 결과는 편의를 위해 보관되지만, 다른 목적으로 사용되지
              않습니다. 사용자가 요청할 경우, 해당 분석 결과는 삭제됩니다.
            </p>
            <br />
            <p class="font-semibold">4. 서비스 이용 기록</p>
            <p>
              4.1 모든 서비스 이용 기록은 서버에 기록됩니다. 이러한 기록은
              서비스의 품질 보증 및 문제 해결을 위해 사용될 수 있습니다.
            </p>
            <p>
              4.2 사용자는 서비스 이용 기록의 기록 및 저장에 동의하며, 이를 통해
              서비스의 개선과 안정성을 유지하기 위한 필요성을 이해합니다.
            </p>
            <br />
            <p class="font-semibold">5. 금지된 행위</p>
            <p>
              5.1 사용자는 본 서비스를 다음과 같은 행위에 이용해서는 안 됩니다:
            </p>
            <ul class="list-disc pl-5">
              <li>불법적인 접근 또는 정보 탈취</li>
              <li>타인의 권리 침해</li>
              <li>서비스의 정상적인 운영을 방해하는 행위</li>
              <li>기타 법령에 위반되는 행위</li>
            </ul>
            <br />
            <p class="font-semibold">6. 약관의 변경</p>
            <p>
              6.1 본 약관은 필요에 따라 변경될 수 있으며, 변경된 약관은 서비스에
              게시됨과 동시에 효력이 발생합니다.
            </p>
            <p>
              6.2 사용자는 변경된 약관에 동의하지 않을 경우, 서비스 이용을
              중단해야 합니다.
            </p>
            <br />
            <p class="font-semibold">7. 법적 책임</p>
            <p>7.1 본 약관은 관련 법률에 따라 해석되고 집행됩니다.</p>
            <p>
              7.2 본 서비스의 이용과 관련하여 발생하는 분쟁은 관할 법원의 재판에
              따릅니다.
            </p>
            <br />
            <p class="font-semibold">8. 연락처</p>
            <p>
              서비스와 관련된 문의 사항이 있으시면 아래의 연락처로 연락 주시기
              바랍니다.
            </p>
            <p>이메일: [sjaqjnjs@gmail.com]</p>
          </div>
          <div class="flex items-center mt-2 4xl:mt-5">
            <input
              type="checkbox"
              checked={$agreedToTerms}
              on:change={handleCheck}
              id="terms-checkbox"
              class="mr-2 4xl:w-5 4xl:h-5 focus:ring-0"
            />
            <label for="terms-checkbox" class="text-sm 4xl:text-lg"
              >개인정보 수집 이용에 동의합니다.</label
            >
          </div>
          <div class="flex justify-center mt-7 w-full 4xl:mt-20">
            <button
              class={`bg-green-500 w-1/4 text-white font-semibold py-2 px-4 4xl:py-3 4xl:text-2xl rounded-lg ${
                $agreedToTerms
                  ? "hover:bg-green-600"
                  : "opacity-80 cursor-not-allowed"
              }`}
              on:click={startInspection}
              disabled={!$agreedToTerms}
            >
              크롤링 시작
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
