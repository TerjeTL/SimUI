<script lang="ts">
	import { Canvas } from '@threlte/core';
	import Scene from '$lib/Scene.svelte';
	import Timeline from '$lib/Timeline.svelte';
	import ForceChart from '$lib/ForceChart.svelte';
	import ColorBar from '$lib/ColorBar.svelte';
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

{#if store.frames.length > 1}
  <!-- <div class="fixed top-6 right-6 rounded-3xl border border-border bg-card/70 backdrop-blur-sm shadow-lg p-4">
    <ForceChart frames={store.frames} currentIndex={store.current} />
  </div> -->
{/if}

{#if store.currentFrame}
  <ColorBar {pmin} {pmax} />
{/if}

<div class="absolute bottom-4 left-8 right-8">
	<Timeline
		bind:frame={store.current}
		total={store.frames.length - 1}
		time={store.currentFrame?.time}
	/>
</div>
