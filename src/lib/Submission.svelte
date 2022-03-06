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
  <div id="submission-title" class="flex space-x-4">
    <div class="text-lg align-bottom">
    <p>{submission.title}</p>
    </div>
    <div class="align-bottom">
    <p>{ts.toLocaleDateString()} {ts.toLocaleTimeString()}</p>
    </div>
  </div>
  <div id="submission-text" >
    <p>{submission_view}</p>
  </div>
</div>
