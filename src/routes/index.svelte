<script context="module">
	export const prerender = true;

    import { username } from './../lib/user'
</script>
<svelte:head>
	<title>OpenPaper</title>
</svelte:head>

{#if $username}
  <h1 class="text-white text-xl p-6 ">Welcome to OpenPaper {$username}!</h1>
  {:else}
  <h1 class="text-white text-xl p-6 ">Welcome to OpenPaper!</h1>
{/if}
