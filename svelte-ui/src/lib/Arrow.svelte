<!-- src/lib/Arrow.svelte -->
<!--
  A single arrow rendered as a line from `origin` in direction `dir`.
  `dir` should be pre-scaled to the desired visual length.
-->
<script lang="ts">
  import { T } from '@threlte/core'
  import { BufferGeometry, BufferAttribute, LineBasicMaterial, Vector3 } from 'three'

  let {
    origin = [0, 0, 0],
    dir    = [0, 1, 0],
    color  = 0xffffff,
  }: {
    origin?: [number, number, number] | Float32Array
    dir?:    [number, number, number] | Float32Array
    color?:  number
  } = $props()

  let geo = $derived.by(() => {
    const g = new BufferGeometry()
    g.setAttribute('position', new BufferAttribute(new Float32Array([
      origin[0], origin[1], origin[2],
      origin[0] + dir[0], origin[1] + dir[1], origin[2] + dir[2],
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