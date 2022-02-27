import { gun } from '../initGun.js';
import { writable } from 'svelte/store';
import { goto } from '$app/navigation';



// The user db
export const user = gun.user().recall({sessionStorage: true});

// Current User's username
export const username = writable('');

user.get('alias').on((v) => username.set(v));

gun.on('auth', async (event) => {
	const alias = await user.get('alias'); // username string
	username.set(alias);
	const pub = await user.get('pub');

	console.log(`signed in as ${alias}`);
	console.log(await user.get('pub'));
});

