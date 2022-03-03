import GUN from "gun";
import Sea from 'gun/sea';

let peers;

//window.sea = Sea;
//window.gun = window.sea.Gun;

if (process.env.NODE_ENV === "development") {
  peers = ["http://localhost:8765/gun"];
} else {
  peers = [];
}

const gun = new GUN({
  peers,
});

//window.gun = gun;
const user = gun.user();

export { gun };
export { GUN };
