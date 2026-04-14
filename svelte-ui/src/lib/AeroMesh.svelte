<!-- src/lib/AeroMesh.svelte -->
<script lang="ts">
  import WireframeMesh from './WireframeMesh.svelte'

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
</script>

<WireframeMesh {vertices} {indices} {color} {opacity} />
