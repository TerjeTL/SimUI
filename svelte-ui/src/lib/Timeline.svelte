<script lang="ts">
  import { Slider } from "bits-ui";

  let { frame = $bindable(), total, time, playing = false, ontoggle }: {
    frame: number
    total: number
    time?: number
    playing?: boolean
    ontoggle?: () => void
  } = $props()

  const MAX_TICKS = 25;

  function niceInterval(rawInterval: number): number {
    const magnitude = Math.pow(10, Math.floor(Math.log10(rawInterval)));
    const n = rawInterval / magnitude;
    if (n <= 1) return magnitude;
    if (n <= 2) return 2 * magnitude;
    if (n <= 5) return 5 * magnitude;
    return 10 * magnitude;
  }

  const tickSet = $derived.by((): Set<number> => {
    if (total <= 1) return new Set([0]);
    const max = total - 1;
    if (total <= MAX_TICKS) {
      return new Set(Array.from({ length: total }, (_, i) => i));
    }
    const interval = niceInterval(max / MAX_TICKS);
    const result = new Set<number>();
    for (let v = 0; v <= max; v += interval) result.add(v);
    result.add(max);
    return result;
  });

  const thumbLabel = $derived(
    time !== undefined ? `${time.toFixed(2)}s` : `${frame}`
  );
</script>

<div class="fixed inset-x-6 bottom-6 rounded-3xl border border-border bg-card/70 backdrop-blur-sm p-8 shadow-lg pointer-events-none">
  <div class="flex items-center gap-6">

  <button
    onclick={ontoggle}
    class="pointer-events-auto shrink-0 text-foreground/70 hover:text-foreground transition-colors"
    aria-label={playing ? 'Pause' : 'Play'}
  >
    {#if playing}
      <!-- pause -->
      <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
        <rect x="4"  y="3" width="4" height="14" rx="1"/>
        <rect x="12" y="3" width="4" height="14" rx="1"/>
      </svg>
    {:else}
      <!-- play -->
      <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
        <polygon points="4,2 18,10 4,18"/>
      </svg>
    {/if}
  </button>

  <Slider.Root
    type="single"
    min={0}
    max={total - 1}
    step={1}
    bind:value={frame}
    class="relative flex grow touch-none select-none items-center pointer-events-auto"
  >
    {#snippet children({ tickItems, thumbItems })}
      <span class="relative h-1.5 grow rounded-full bg-muted">
        <Slider.Range class="absolute h-full rounded-full bg-primary" />

        {#each tickItems as { value: tickValue, index } (index)}
          {#if tickSet.has(tickValue)}
            <Slider.Tick
              {index}
              class="absolute top-1/2 h-3 w-px -translate-y-1/2 bg-border data-[bounded]:bg-primary"
            />
            <Slider.TickLabel
              {index}
              position="bottom"
              class="mt-2 text-[10px] tabular-nums text-muted-foreground"
            >
              {tickValue}
            </Slider.TickLabel>
          {/if}
        {/each}
      </span>

      {#each thumbItems as { index } (index)}
        <Slider.ThumbLabel
          {index}
          position="top"
          class="mb-2 text-xs font-semibold tabular-nums text-foreground"
        >
          {thumbLabel}
        </Slider.ThumbLabel>
        <Slider.Thumb
          {index}
          class="block size-4 rounded-full border-2 border-primary bg-background shadow outline-none"
        />
      {/each}
    {/snippet}
  </Slider.Root>

  </div>
</div>
