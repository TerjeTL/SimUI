<!-- src/lib/RigLine.svelte — line segment between two world-space NED points -->
<script lang="ts">
  import { T } from '@threlte/core'
  import { BufferGeometry, BufferAttribute, LineBasicMaterial } from 'three'

  let {
    a,
    b,
    color = 0xffffff,
  }: {
    a:      Float32Array | [number, number, number]
    b:      Float32Array | [number, number, number]
    color?: number
  } = $props()

  let geo = $derived.by(() => {
    const g = new BufferGeometry()
    g.setAttribute('position', new BufferAttribute(new Float32Array([
      a[0], a[1], a[2],
      b[0], b[1], b[2],
    ]), 3))
    return g
  })

  let mat = $derived(new LineBasicMaterial({ color }))

  $effect(() => {
    const g = geo
    return () => g.dispose()
  })
</script>

<T.Line geometry={geo} material={mat} />
