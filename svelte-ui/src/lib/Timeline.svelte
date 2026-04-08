<script lang="ts">
  import { Slider } from "bits-ui";

  let { frame = $bindable(), total, time }: {
    frame: number
    total: number
    time?: number
  } = $props()

  const MAX_TICKS = 101;
  function showTick(index: number, total: number): boolean {
    if (total <= MAX_TICKS) return true;
    const stride = Math.ceil((total - 1) / (MAX_TICKS - 1));
    return index % stride === 0 || index === total - 1;
  }
</script>

<div class="fixed inset-x-6 bottom-6 rounded-3xl border border-border bg-card p-8 shadow-lg">
  <Slider.Root
    type="single"
    step={total}
    bind:value={frame}
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
          {#if showTick(index, tickItems.length)}
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

      {#each thumbItems as { value: thumbValue, index } (index)}
        <Slider.ThumbLabel
          {index}
          position="top"
          class="mb-2 text-xs font-semibold tabular-nums text-foreground"
        >
          {thumbValue.toFixed(2)}s
        </Slider.ThumbLabel>
        <Slider.Thumb
          {index}
          class="block size-4 rounded-full border-2 border-primary bg-background shadow"
        />
      {/each}
    {/snippet}
  </Slider.Root>
</div>