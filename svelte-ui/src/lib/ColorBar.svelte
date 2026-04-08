<!-- src/lib/ColorBar.svelte -->
<script lang="ts">
  import { lutCSS } from './colormap'

  let { pmin, pmax }: { pmin: number; pmax: number } = $props()

  const gradient = $derived(
    'linear-gradient(to top, ' +
    Array.from({ length: 12 }, (_, i) => lutCSS(i / 11)).join(',') +
    ')'
  )

  function niceTicks(min: number, max: number, count = 7): number[] {
    const rawStep = (max - min) / (count - 1)
    const mag  = Math.pow(10, Math.floor(Math.log10(rawStep)))
    const n    = rawStep / mag
    const step = n <= 1 ? mag : n <= 2 ? 2 * mag : n <= 5 ? 5 * mag : 10 * mag
    const start = Math.ceil(min / step) * step
    const ticks: number[] = []
    for (let v = start; v <= max + step * 0.01; v += step) ticks.push(parseFloat(v.toPrecision(10)))
    return ticks
  }

  // Recover the true data range from the padded values (pad = true_range * 0.1,
  // so pmax - pmin = true_range * 1.2, pad = (pmax - pmin) / 12).
  // Generate ticks within the true range so the 10% margins stay symmetric.
  const ticks = $derived.by(() => {
    const pad     = (pmax - pmin) / 12
    const trueMin = pmin + pad
    const trueMax = pmax - pad
    return niceTicks(trueMin, trueMax)
  })

  function pct(val: number): string {
    return `${(1 - (val - pmin) / (pmax - pmin)) * 100}%`
  }

  function fmt(v: number): string {
    if (Math.abs(v) >= 1000)  return (v / 1000).toFixed(1) + 'k'
    if (Number.isInteger(v))  return v.toFixed(0)
    return v.toFixed(1)
  }
</script>

<div class="fixed right-0 top-1/2 -translate-y-1/2 flex items-start">
  <!-- gradient bar -->
  <div class="w-5 h-[33vh] rounded-[2px] shrink-0" style="background: {gradient}"></div>

  <!-- tick marks + labels, absolutely positioned along bar height -->
  <div class="relative h-[33vh] w-12">
    {#each ticks as tick}
      <div
        class="absolute left-0 right-0 flex items-center"
        style="top: {pct(tick)}; transform: translateY(-50%)"
      >
        <div class="w-2 h-px bg-muted-foreground/60 flex-shrink-0"></div>
        <span class="ml-1 text-[10px] tabular-nums font-mono text-muted-foreground [text-shadow:0_0_4px_var(--background),0_0_4px_var(--background)]">
          {fmt(tick)}
        </span>
      </div>
    {/each}
  </div>
</div>
