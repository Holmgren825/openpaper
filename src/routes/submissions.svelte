<script>
  import { gun, GUN } from './../initGun';
  import { user, username } from './../lib/user';
  import { onMount } from 'svelte'
  import Submission from '../lib/Submission.svelte'

  let new_submission;
  let new_title;
  let submissions = [];

  function on_submit(){
    console.log("Log: Submit")
    console.log(new_submission)
    const what = new_submission
    const submission = user.get('all').set({what: what, title: new_title})
    const index = new Date().toISOString();
    gun.get('submissions').get(index).put(submission);

    // Clear fields
    new_submission = ""
    new_title = ""
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
          title: (await data.title) + '',
          when: GUN.state.is(data, 'what')
      };
      if (submission.what) {
        submissions = [...submissions.slice(-100), submission].sort((a, b) => a.when - b.when);
        }
    }
  });

  });


</script>

<div class="text-white p-2 py-2 mx-2 max-w-5xl">
  {#if $username}
  <div>
    <h1 class="text-xl">New Submission</h1>
  </div>
    <div>
    <form on:submit|preventDefault={on_submit}>
      <div>
      <input
        type="text"
        class="text-white h-15 w-full border-2 rounded-lg border-white my-2 p-2 bg-neutral-800"
        placeholder="Set title..."
        bind:value={new_title}
        />
      </div>
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
          disabled={!new_submission || !$username}
          >
          Submit
          </button>
      </div>
    </form>
    </div>
  {/if}
  <div class="py-4">
    <h1 class="text-xl">Previous submissions</h1>
    {#each submissions as submission, index (submission.when)}
      <Submission {submission}/>
    {/each}
  </div>
</div>
