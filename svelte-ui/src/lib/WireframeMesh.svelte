<!-- src/lib/WireframeMesh.svelte -->
<script lang="ts">
  import { T } from '@threlte/core'
  import { BufferGeometry, BufferAttribute } from 'three'

  let {
    vertices,
    indices,
    color   = 0xcccccc,
    opacity = 1.0,
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
  <T.MeshBasicMaterial
    {color}
    wireframe
    transparent={opacity < 1}
    {opacity}
  />
</T.Mesh>
