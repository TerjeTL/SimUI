<script lang="ts">
	import { Canvas } from '@threlte/core';
	import Scene from '$lib/Scene.svelte';
	import Timeline from '$lib/Timeline.svelte';
	import { FrameStore, fromSimData, isComplete } from '$lib/frame.svelte';
	import type { SimData } from './simdata.ts';

	const store = new FrameStore();
	let pending = $state<Partial<SimData>>({});

	window.onData = (key, value) => {
		// Reset accumulator when a new frame starts (index field arrives first)
		if (key === 'index') pending = {};

		pending[key] = value;

		if (isComplete(pending)) {
			store.add(fromSimData(pending));
			pending = {};
		}
	};
</script>

<Canvas><Scene frame={store.currentFrame} /></Canvas>

<div class="absolute bottom-4 left-8 right-8">
	<Timeline
		bind:frame={store.current}
		total={store.frames.length - 1}
		time={store.currentFrame?.time}
	/>
</div>