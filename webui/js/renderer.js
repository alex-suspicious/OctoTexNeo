import * as THREE from 'three';

import Stats from 'three/addons/libs/stats.module.js';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';

let camera, controls, scene, renderer, stats;

let mesh, geometry, material, clock;

const worldWidth = 128, worldDepth = 128;

let moveForward = false;
let moveBackward = false;
let moveLeft = false;
let moveRight = false;
let canJump = false;

let prevTime = performance.now();
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();
const vertex = new THREE.Vector3();

init();
animate();

function init() {

	camera = new THREE.PerspectiveCamera( 60, window.innerWidth / window.innerHeight, 1, 20000 );
	camera.position.y = 0;

	clock = new THREE.Clock();

	scene = new THREE.Scene();
	scene.background = new THREE.Color( 0x141414 );
	//scene.fog = new THREE.FogExp2( 0xAAAAAA, 0.0007 );

	const grid = new THREE.GridHelper( 200, 40, 0xAAAAAA, 0xAAAAAA );
	grid.material.opacity = 0.5;
	grid.material.transparent = true;
	scene.add( grid );


	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( $(".renderer").width(), $(".renderer").height() );
	$(".renderer").append( renderer.domElement );

	controls = new PointerLockControls( camera, renderer.domElement );



	controls.addEventListener( 'lock', function () {

	} );

	controls.addEventListener( 'unlock', function () {

	} );

	scene.add( controls.getObject() );


	const onKeyDown = function ( event ) {

		switch ( event.code ) {

			case 'ArrowUp':
			case 'KeyW':
				moveForward = true;
				break;

			case 'ArrowLeft':
			case 'KeyA':
				moveLeft = true;
				break;

			case 'ArrowDown':
			case 'KeyS':
				moveBackward = true;
				break;

			case 'ArrowRight':
			case 'KeyD':
				moveRight = true;
				break;
		}

	};

	const onKeyUp = function ( event ) {

		switch ( event.code ) {

			case 'ArrowUp':
			case 'KeyW':
				moveForward = false;
				break;

			case 'ArrowLeft':
			case 'KeyA':
				moveLeft = false;
				break;

			case 'ArrowDown':
			case 'KeyS':
				moveBackward = false;
				break;

			case 'ArrowRight':
			case 'KeyD':
				moveRight = false;
				break;

		}

	};


	document.addEventListener( 'keydown', onKeyDown );
	document.addEventListener( 'keyup', onKeyUp );

	stats = new Stats();
	$(".fps-counter").append( stats.dom );

	//

	window.addEventListener( 'resize', onWindowResize );

}

function onWindowResize() {

	camera.aspect = $(".renderer").width() / $(".renderer").height();
	camera.updateProjectionMatrix();

	renderer.setSize( $(".renderer").width(), $(".renderer").height() );

	controls.handleResize();

}

$(".renderer").bind("contextmenu",function(e){
   return false;
}); 

$(".renderer").mousedown(function(event) {
    switch (event.which) {
        case 1:
           	//alert('Left Mouse button pressed.');
            break;
        case 2:
            //alert('Middle Mouse button pressed.');
            break;
        case 3:
            controls.lock();
            break;
        default:
            break;
    }
});


$(".renderer").mouseup(function(event) {
    switch (event.which) {
        case 1:
           	//alert('Left Mouse button pressed.');
            break;
        case 2:
            //alert('Middle Mouse button pressed.');
            break;
        case 3:
            controls.unlock();
            break;
        default:
            break;
    }
});

function animate() {
	const time = performance.now();
	requestAnimationFrame( animate );

	const delta = ( time - prevTime ) / 1000;
	//const cameraDir = controls.getDirection();

	velocity.x = 0;
	velocity.z = 0;
	velocity.y = 0;

	direction.z = Number( moveForward ) - Number( moveBackward );
	direction.x = Number( moveRight ) - Number( moveLeft );
	direction.normalize(); // this ensures consistent movements in all directions

	if ( moveForward || moveBackward ) velocity.z -= direction.z * 20500.0 * delta;
	if ( moveLeft || moveRight ) velocity.x -= direction.x * 20500.0 * delta;

	controls.moveRight( - velocity.x * delta );

	var mouse3D = new THREE.Vector3();
	mouse3D.normalize();
	controls.getDirection( mouse3D );


	controls.getObject().position.x = controls.getObject().position.x + (mouse3D.x*direction.z);
	controls.getObject().position.y = controls.getObject().position.y + (mouse3D.y*direction.z);
	controls.getObject().position.z = controls.getObject().position.z + (mouse3D.z*direction.z);

	prevTime = time;
	render();
	stats.update();

}

function render() {

	const delta = clock.getDelta();
	const time = clock.getElapsedTime() * 10;


	//controls.update( delta );
	renderer.render( scene, camera );

}