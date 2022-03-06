<script>
  import { gun, GUN } from './../initGun';
  import { user, username } from './../lib/user';

  let new_submission;
  let new_title;
  let base_stake = 100;
  let added_stake;

  function on_submit(){
    console.log("Log: Submit")
    console.log(new_submission)
    const what = new_submission
    const accepted = false;
    const rejected = false;
    const stake = base_stake + added_stake;
    const submission = user.get('all').set({what: what, title: new_title, stake: stake, accepted: accepted, rejected: rejected})
    const index = new Date().toISOString();
    gun.get('submissions').get(index).put(submission);

    // Clear fields
    new_submission = ""
    new_title = ""
    added_stake = ""
  }

</script>
{#if $username}
<div class="p-6 max-w-5xl text-white">
<div>
  <h1 class="text-xl">New Submission</h1>
</div>
  <div>
  <form on:submit|preventDefault={on_submit}>
    <div class="flex justify-between space-x-4">
    <input
      type="text"
      class="text-white h-15 w-full border-2 rounded-lg border-white my-2 p-2 bg-neutral-800"
      placeholder="Title..."
      bind:value={new_title}
      />
    <input
      type="number"
      class="text-white h-15 w-3/12 border-2 rounded-lg border-white my-2 p-2 bg-neutral-800"
      placeholder="Added stake..."
      bind:value={added_stake}
      />
    </div>
    <div>
    <textarea 
      class="text-white h-64 w-full border-2 rounded-lg border-white my-2 p-2 bg-neutral-800"
      placeholder="Abstract..."
      bind:value={new_submission}
      ></textarea>
    </div>
    <div class="my-2 flex justify-between">
    <div class="space-y-2">
    <h1>Upload document</h1>
    <input type="file" accept=".pdf"/>
    </div>
    <button 
        class="w-4/12 border-2 rounded-lg border-white py-2 bg-neutral-800 hover:bg-sky-500 hover:border-sky-500"
        on:click={on_submit}
        type="submit"
        disabled={!new_submission || !new_title || !$username}
        >
        Submit
        </button>
    </div>
  </form>
</div>
</div>
{:else}
<div class="p-6 max-w-5xl text-white">
  Please sign in!
</div>

{/if}
