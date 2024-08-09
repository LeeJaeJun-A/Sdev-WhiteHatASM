<script lang="ts">
  import NavBar from "$lib/components/NavBar.svelte";
  import { Contact } from "flowbite-svelte-blocks";
  import { Label, Input, Textarea, Button } from "flowbite-svelte";
  import { writable } from "svelte/store";

  const email = writable<string>("");
  const phone_number = writable<string>("");
  const subject = writable<string>("");
  const message = writable<string>("");

  let emailError = writable<string | null>(null);
  let phoneError = writable<string | null>(null);

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const phoneRegex = /^010-\d{4}-\d{4}$/;

  const handleSubmit = (event: Event) => {
    event.preventDefault();

    let valid = true;

    if (!emailRegex.test($email)) {
      emailError.set("유효한 이메일 주소를 입력해 주세요.");
      valid = false;
    } else {
      emailError.set(null);
    }

    if (!phoneRegex.test($phone_number)) {
      phoneError.set(
        "유효한 전화번호 형식을 입력해 주세요. (예: 010-1234-5678)"
      );
      valid = false;
    } else {
      phoneError.set(null);
    }

    if (valid) {
      console.log("Email:", $email);
      console.log("Phone Number:", $phone_number);
      console.log("Subject:", $subject);
      console.log("Message:", $message);
    }
  };
</script>

<main class="bg-white w-screen h-screen">
  <NavBar />
  <div class="w-full flex justify-center items-center p-2 select-none" style="height: 92%;">
    <div class="w-full h-full flex flex-col justify-center items-center">
      <Contact class="w-1/3">
        <p
          class="w-1/3 text-4xl flex justify-center items-center font-semibold 4xl:text-6xl max-h-24"
          style="height: 10%"
        >
          Contact Us
        </p>
        <p
          class="text-center text-gray-500 w-1/3 flex justify-center items-center 4xl:text-2xl max-h-24 text-sm"
          style="height: 10%;"
        >
          문제가 있거나 계정을 얻고 싶거나 비밀번호를 까먹었을 때,<br />
          또는 기타 문의사항이 있으시면 언제든지 연락해 주세요.
        </p>
        <form
          on:submit={handleSubmit}
          class="space-y-2 flex text-sm flex-col justify-center items-center w-1/3 4xl:space-y-7"
          style="height: 78%;"
        >
          <div class="w-full">
            <Label for="email" class="block mb-1 4xl:text-xl 4xl:mb-2"
              >이메일</Label
            >
            <Input
              id="email"
              name="email"
              placeholder="example@google.com"
              bind:value={$email}
              class="w-full 4xl:text-xl"
              required
            />
            {#if $emailError}
              <p class="text-red-500 text-sm">{$emailError}</p>
            {/if}
          </div>
          <div class="w-full">
            <Label for="phone_number" class="block mb-1 4xl:text-xl 4xl:mb-2"
              >전화번호</Label
            >
            <Input
              id="phone_number"
              name="phone_number"
              placeholder="010-1234-5678"
              bind:value={$phone_number}
              class="w-full 4xl:text-xl"
              required
            />
            {#if $phoneError}
              <p class="text-red-500 text-sm">{$phoneError}</p>
            {/if}
          </div>
          <div class="w-full">
            <Label for="subject" class="block mb-1 4xl:text-xl 4xl:mb-2"
              >제목</Label
            >
            <Input
              id="subject"
              name="subject"
              placeholder="도와드릴 사항을 알려주세요"
              bind:value={$subject}
              class="w-full 4xl:text-xl"
              required
            />
          </div>
          <div class="w-full">
            <Textarea
              id="message"
              name="message"
              placeholder="메시지를 남겨주세요..."
              label="메시지"
              bind:value={$message}
              maxlength="600"
              class="w-full h-32 resize-none overflow-auto 4xl:h-96 4xl:text-xl"
            />
            <p class="text-gray-500 text-sm">
              {$message.length}/600 characters used
            </p>
          </div>
          <Button type="submit" class="4xl:text-xl w-1/3">메시지 보내기</Button>
        </form>
      </Contact>
    </div>
  </div>
</main>
