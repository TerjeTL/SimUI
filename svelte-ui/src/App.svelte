<script lang="ts">
	import { Canvas } from '@threlte/core';
	import Scene from '$lib/Scene.svelte';
	import Timeline from '$lib/Timeline.svelte';
	import ColorBar from '$lib/ColorBar.svelte';
	import { FrameStore } from '$lib/frame.svelte';
	import { fromEncoded, type EncodedFrame } from './frame.ts';

	const store = new FrameStore();

	let playing       = $state(false);
	let playbackSpeed = $state(4);
	let raf = -1;

	function play() {
		if (playing) return;
		playing = true;
		const startIdx     = store.current;
		const startSimTime = store.frames[startIdx]?.time ?? 0;
		const wallStart    = performance.now();

		function tick() {
			const target = startSimTime + (performance.now() - wallStart) / 1000 * playbackSpeed;
			let idx = store.current;
			while (idx < store.frames.length - 1 && (store.frames[idx + 1].time ?? 0) <= target)
				idx++;
			store.current = idx;
			if (idx >= store.frames.length - 1) { playing = false; return; }
			raf = requestAnimationFrame(tick);
		}
		raf = requestAnimationFrame(tick);
	}

	function pause() {
		playing = false;
		cancelAnimationFrame(raf);
	}

	window.onFrame = (d: EncodedFrame) => store.add(fromEncoded(d));

	// Global pressure range across all frames, padded 10% beyond true min/max
	let pressureRange = $derived.by(() => {
		let mn = Infinity, mx = -Infinity
		for (const f of store.frames)
			for (let i = 0; i < f.facePressure.length; i++) {
				if (f.facePressure[i] < mn) mn = f.facePressure[i]
				if (f.facePressure[i] > mx) mx = f.facePressure[i]
			}
		if (mn === Infinity) return { pmin: 0, pmax: 1 }
		const pad = (mx - mn) * 0.1
		return { pmin: mn - pad, pmax: mx + pad }
	})

	let pmin = $derived(pressureRange.pmin)
	let pmax = $derived(pressureRange.pmax)
</script>

<Canvas><Scene frame={store.currentFrame} {pmin} {pmax} /></Canvas>

{#if store.currentFrame}
  <ColorBar {pmin} {pmax} />
{/if}

<div class="absolute bottom-4 left-8 right-8">
	<Timeline
		bind:frame={store.current}
		total={store.frames.length - 1}
		time={store.currentFrame?.time}
		{playing}
		ontoggle={() => playing ? pause() : play()}
	/>
</div>
