<!-- src/lib/ForceChart.svelte -->
<script lang="ts">
  import { onMount } from 'svelte'
  import uPlot from 'uplot'
  import 'uplot/dist/uPlot.min.css'
  import type { HullFrame } from './frame.svelte.ts'

  let {
    frames,
    currentIndex,
  }: {
    frames:       HullFrame[]
    currentIndex: number
  } = $props()

  let el: HTMLDivElement

  let u: uPlot | null = null

  function buildData(frames: HullFrame[]): uPlot.AlignedData {
    const xs: number[] = []
    const ys: number[] = []
    for (const f of frames) {
      const t = f.time ?? f.index / 120
      let total = 0
      for (let i = 0; i < f.facePressure.length; i++) total += f.facePressure[i]
      xs.push(t)
      ys.push(total)
    }
    return [xs, ys]
  }

  const opts: uPlot.Options = {
    width:  300,
    height: 110,
    scales: { x: { time: false } },
    series: [
      {},
      {
        label:  'F_hydro',
        stroke: '#38bdf8',
        width:  1.5,
      },
    ],
    axes: [
      { label: 't (s)', labelSize: 16, size: 28 },
      { label: 'N',     labelSize: 16, size: 52 },
    ],
    legend: { show: false },
    cursor: { drag: { x: false, y: false } },
  }

  onMount(() => {
    u = new uPlot(opts, buildData(frames), el)
    return () => u?.destroy()
  })

  // update series data as new frames arrive
  $effect(() => {
    if (!u) return
    u.setData(buildData(frames))
  })

  // sync cursor line to timeline position
  $effect(() => {
    if (!u || !frames[currentIndex]) return
    const t    = frames[currentIndex].time ?? frames[currentIndex].index / 120
    const left = u.valToPos(t, 'x')
    u.setCursor({ left, top: opts.height! / 2 })
  })
</script>

<div bind:this={el}></div>
