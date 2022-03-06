<script>
	import { page } from '$app/stores';
	import logo from './bird_icon.svg';
    import { username, user } from '../user';

    function signout() {
      user.leave();
      username.set('');
    }
</script>

<header>
  <nav class="bg-gradient-to-r from-emerald-500 to-emerald-900">
    <div class="p-2  mx-auto">
      <div class="flex items-center justify-center sm:justify-start">
      <div>
        <img class="h-14 w-14" src={logo} alt="OpenPaper Logo">
      </div>
      <div class="flex space-x-4">
        <a class="hover:bg-black hover:bg-opacity-10 hover:text-white px-2 py-2 rounded-md font-medium" sveltekit:prefetch href="/">Home</a>
        <a class="hover:bg-black hover:bg-opacity-10 hover:text-white px-2 py-2 rounded-md font-medium" sveltekit:prefetch href="/submissions">Read</a>
        {#if !$username}
        <a class="hover:bg-black hover:bg-opacity-10 hover:text-white px-2 py-2 rounded-md font-medium" sveltekit:prefetch href="/auth">Sign in</a>
        {/if}
        {#if $username}
        <button class="hover:bg-black hover:bg-opacity-10 hover:text-white px-2 py-2 rounded-md font-medium" on:click={signout} >Sign out</button>
        {/if}
        <a class="hover:bg-black hover:bg-opacity-10 hover:text-white px-2 py-2 rounded-md font-medium"  sveltekit:prefetch href="/about">About</a>
      </div>
      </div>
    </div>
  </nav>
</header>
