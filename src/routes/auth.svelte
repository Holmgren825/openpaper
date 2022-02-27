<script>
  import { user } from '../lib/user';
  import { goto } from '$app/navigation';
  let username;
  let password;
  let loginErr;
  let signupErr;


  function login() {
      console.log('Log: Try login')
      user.auth(username, password, ({ err }) => {
          if (err) {
              //alert(err);
              username = '';
              password = '';
              loginErr = err;
          } else {
              goto(`/`);
              // Current User's username

              //user.get('alias').on((v) => username.set(v));
          }
      });
  }
  function signup() {
      console.log('Log: Try signup')
    	user.create(username, password, ({ err }) => {
    		if (err) {
    			//alert(err);
    			signupErr = err;
    			username = '';
    			password = '';
    		} else {
    			login();
    		}
    	});
    }
    function logout() {
    user.leave();
    username.set('');
    }
</script>

<h1 class="text-white text-xl p-2 py-3 mx-2">Sign in</h1>
<div class="w-3/12">
<div class="p-2 px-4 mx-auto text-white"> 
  <input 
    type="text"
    placeholder="Username"
    bind:value={username}
    class="border-2 rounded-full border-white p-2 bg-neutral-800 w-full"
    />
</div>
<div class="p-2 px-4 mx-auto text-white"> 
  <input 
    type="password"
    placeholder="Password"
    bind:value={password}
    class="border-2 rounded-full border-white p-2 bg-neutral-800 w-full"
    />
</div>
<div class="flex justify-between space-x-4 text-white p-2 px-4">
    <button class="w-5/12 border-2 rounded-full border-white py-1 bg-neutral-800 hover:bg-gray-500" on:click={login}>Sign in </button>
    <button class="w-5/12 border-2 rounded-full border-white py-1 bg-neutral-800 hover:bg-gray-500"  on:click={signup}>Sign up </button>
</div>
</div>
