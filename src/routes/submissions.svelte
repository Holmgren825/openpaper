<script>
  import { gun } from './../initGun';
  import { user, username } from './../lib/user';
  import { onMount } from 'svelte'

  let new_submission;
  let submissions = [];

  function on_submit(){
    console.log("Log: Submit")
    console.log(new_submission)
    const what = new_submission
    const submission = user.get('all').set({what: what})
    const index = new Date().toISOString();
    gun.get('submissions').get(index).put(submission);
  }

  onMount(() => {
    var match = {
      // lexical queries are kind of like a limited RegEx or Glob.
      '.': {
      // property selector
      '>': new Date(+new Date() - 1 * 1000 * 60 * 60 * 3).toISOString(), // find any indexed property larger ~3 hours ago
      },
      '-': 1, // filter in reverse
    };
    gun.get('submissions')
      .map(match)
      .once(async (data, id) => {
      if (data) {

        var submission = {
          who: await gun.user(data).get('alias'),
          what: (await data.what) + '',
      };
      if (submission.what) {
        submissions = [...submissions.slice(-100), submission];
        }
    }
  });

  });


</script>

<div class="text-white p-2 py-2 mx-2 max-w-5xl">
  <div>
    <h1 class="text-xl">Submissions</h1>
  </div>
  {#if $username}
    <div>
    <form on:submit|preventDefault>
      <div>
      <textarea 
        class="text-white h-40 w-full border-2 rounded-lg border-white my-2 p-2 bg-neutral-800"
        placeholder="Write something..."
        bind:value={new_submission}
        ></textarea>
      </div>
      <div>
      <button 
          class="w-4/12 border-2 rounded-lg border-white py-2 bg-neutral-800 hover:bg-gray-500"
          on:click={on_submit}
          type="submit"
          disabled={!new_submission}
          >
          Submit
          </button>
      </div>
    </form>
    </div>
  {/if}
  <div class="py-4">
    <h1 class="text-xl">Previous submissions</h1>
    {#each submissions as submission (submission)}
      <p>{submission.who} {submission.what}</p>
    {/each}
  </div>
</div>
