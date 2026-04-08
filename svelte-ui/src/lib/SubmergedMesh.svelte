<!-- src/lib/SubmergedMesh.svelte -->
<script lang="ts">
  import { T } from '@threlte/core'
  import { BufferGeometry, BufferAttribute } from 'three'

  let {
    vertices,
    indices,
  }: {
    vertices: Float32Array
    indices:  Uint32Array
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
  <T.MeshBasicMaterial color={0x00aaff} wireframe />
</T.Mesh>
