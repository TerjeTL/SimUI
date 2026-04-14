<!-- src/lib/Sail.svelte — sail strip mesh, world-space NED coordinates -->
<!-- vertices: Float32Array (n*4 × 3 flat), indices: Uint32Array (n*2 × 3 flat) -->
<script lang="ts">
  import { T } from '@threlte/core'
  import { BufferGeometry, BufferAttribute, DoubleSide } from 'three'

  let {
    vertices,
    indices,
    color   = 0xf5f0e8,
    opacity = 0.75,
  }: {
    vertices: Float32Array
    indices:  Uint32Array
    color?:   number
    opacity?: number
  } = $props()

  let geo = $derived.by(() => {
    const g = new BufferGeometry()
    g.setAttribute('position', new BufferAttribute(vertices, 3))
    g.setIndex(new BufferAttribute(indices, 1))
    return g
  })

  $effect(() => {
    const g = geo
    return () => g.dispose()
  })
</script>

<T.Mesh geometry={geo}>
  <T.MeshLambertMaterial
    {color}
    transparent={opacity < 1}
    {opacity}
    side={DoubleSide}
  />
</T.Mesh>
