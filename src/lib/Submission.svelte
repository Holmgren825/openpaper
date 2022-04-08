<script>
  export let submission;
  //export let creator;


  // const submissionClass = submission.who === creator;
  
  let submission_short = submission.what.substring(0,320) + " ...";

  let submission_view = submission_short;
  let submission_view_state = true;

  function change_submission_state(){
    if (submission_view_state) {
      submission_view = submission.what;
    } else {
      submission_view = submission_short;
    };
    submission_view_state = !submission_view_state;

}

   const ts = new Date(submission.when);
</script>

<div class="p-2 hover:rounded-lg hover:border-white hover:border-2 overflow-visible"
     on:click={change_submission_state}
  >
  <div id="submission-title" class="flex space-x-4 items-end py-2">
    <div class="text-xl">
      <p>{submission.title}</p>
    </div>
    <div>
      <p>{ts.toLocaleDateString()} {ts.toLocaleTimeString()}</p>
    </div>
  <div>
        {#if submission.accepted}
        <div class="rounded-lg border-2 px-2 bg-green-500">
          <p>Accepted</p>
       </div>
        {/if}
        {#if !submission.accepted}
        <div class="rounded-lg px-2 bg-orange-500">
          <p>In review</p>
       </div>
        {/if}
    </div>
  </div>
  <div id="submission-text" >
    <p>{submission_view}</p>
  </div>
</div>
