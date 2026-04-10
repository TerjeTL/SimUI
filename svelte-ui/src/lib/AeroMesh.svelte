<!-- src/lib/AeroMesh.svelte -->
<script lang="ts">
  import SubmergedMesh from './SubmergedMesh.svelte'

  let {
    vertices,
    indices,
    color   = 0xcccccc,
    opacity = 1.0,
    wireframe = true,
  }: {
    vertices:   Float32Array
    indices:    Uint32Array
    color?:     number
    opacity?:   number
    wireframe?: boolean
  } = $props()
</script>

<SubmergedMesh
  {vertices}
  {indices}
  {color}
  {opacity}
  {wireframe}
  polygonOffset={true}
  polygonOffsetFactor={1}
  polygonOffsetUnits={1}
/>
