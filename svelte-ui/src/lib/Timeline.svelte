<script lang="ts">
  import { Slider } from "bits-ui";

  let { frame = $bindable(), total, time }: {
    frame: number
    total: number
    time?: number
  } = $props()

  const MAX_TICKS = 100;

  // step as array makes bits-ui generate tickItems at exactly these positions
  const step = $derived(
    total <= MAX_TICKS
      ? Array.from({ length: total }, (_, i) => i)
      : Array.from({ length: MAX_TICKS }, (_, i) =>
          Math.round(i * (total - 1) / (MAX_TICKS - 1))
        )
  );
</script>

<div class="fixed inset-x-6 bottom-6 rounded-3xl border border-border bg-card p-8 shadow-lg">
  <Slider.Root
    type="single"
    min={0}
    max={total - 1}
    bind:value={frame}
    {step}
    class="relative flex w-full touch-none select-none items-center"
  >
    {#snippet children({ tickItems, thumbItems })}
      <span class="relative h-1.5 grow rounded-full bg-muted">
        <Slider.Range class="absolute h-full rounded-full bg-primary" />

        {#each tickItems as { value: tickValue, index } (index)}
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
        {/each}
      </span>

      {#each thumbItems as { index } (index)}
        {#if time !== undefined}
          <Slider.ThumbLabel
            {index}
            position="top"
            class="mb-2 text-xs font-semibold tabular-nums text-foreground"
          >
            {time.toFixed(2)}s
          </Slider.ThumbLabel>
        {/if}
        <Slider.Thumb
          {index}
          class="block size-4 rounded-full border-2 border-primary bg-background shadow"
        />
      {/each}
    {/snippet}
  </Slider.Root>
</div>