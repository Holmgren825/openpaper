<script>
  import { gun, GUN } from './../initGun';
  import { onMount } from 'svelte'
  import Submission from '../lib/Submission.svelte'
  import { user, username } from './../lib/user';
  import { goto } from '$app/navigation';

  let submissions = [];

  onMount(() => {
    gun.get('submissions')
      .map()
      .once(async (data, id) => {
      if (data) {

        var submission = {
          who: await gun.user(data).get('alias'),
          what: (await data.what),
          title: (await data.title),
          when: GUN.state.is(data, 'what'),
          accepted: data.accepted,
      };
      if (submission.what) {
        submissions = [...submissions.slice(-100), submission].sort((a, b) => new Date(b.when)-new Date(a.when));
        }
    }
  });

  });

  function new_submission(){
    if (!user.is) {
      goto("auth")
  } else {
      goto("new_submission")
  }
}
</script>

<div class="flex text-white p-6 max-w-5xl justify-between items-end">
  <div class="">
  <h1 class="text-xl">Published</h1>
  </div>
  <div>
    <button class="rounded-lg border-2 border-sky-500 p-1 bg-sky-500 hover:bg-sky-400 hover:sky-400 " on:click={new_submission}>New submission</button>
  </div>
</div>
<div>
  <hr>
</div>
<div class="text-white px-4 py-2 max-w-5xl">
  {#each submissions as submission (submission.when) }
    <Submission {submission}/>
  {/each}
</div>
