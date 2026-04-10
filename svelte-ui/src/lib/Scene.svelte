<!-- src/lib/Scene.svelte -->
<script lang="ts">
  import { T } from '@threlte/core'
  import { OrbitControls } from '@threlte/extras'
  import type { OrbitControls as ThreeOrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
  import type { HullFrame } from './frame.svelte.ts'
  import SubmergedMesh from '$lib/SubmergedMesh.svelte'
  import AeroMesh      from '$lib/AeroMesh.svelte'
  import HydroForces   from '$lib/HydroForces.svelte'
  import AxisGizmo     from '$lib/AxisGizmo.svelte'
  let {
    frame,
    pmin,
    pmax,
    showForces = true,
  }: {
    frame:       HullFrame | null
    pmin?:       number
    pmax?:       number
    showForces?: boolean
  } = $props()

  let controls: ThreeOrbitControls | undefined = $state()

  // Follow the hull: mutate controls.target in-place (do NOT replace the reference —
  // OrbitControls keeps internal spherical state relative to the original object).
  // Also shift the camera by the same delta so the view angle is preserved.
  $effect(() => {
    if (!controls || !frame) return
    const nx =  frame.position[0]
    const ny = -frame.position[2]   // NED Z-down → Three.js -Y
    const nz =  frame.position[1]   // NED Y-right → Three.js +Z
    const dx = nx - controls.target.x
    const dy = ny - controls.target.y
    const dz = nz - controls.target.z
    controls.target.set(nx, ny, nz)
    controls.object.position.x += dx
    controls.object.position.y += dy
    controls.object.position.z += dz
  })
</script>

<T.PerspectiveCamera makeDefault position={[10, 5, 10]}>
  <OrbitControls bind:ref={controls} />
</T.PerspectiveCamera>

<T.DirectionalLight position={[3, 10, 7]} />
<T.AmbientLight intensity={0.4} />

<!--
  NED → Three.js coordinate remap (applied once here).
  Rx(+90°): NED X→X,  NED Y→+Z,  NED Z→−Y
  Waterline at Y=0; submerged geometry at Y<0.
  All child components author in NED space.
-->
<T.Group rotation={[Math.PI / 2, 0, 0]}>
  <AxisGizmo scale={3} />

  {#if frame}
    <SubmergedMesh
      vertices={frame.vertices}
      indices={frame.indices}
      facePressure={frame.facePressure}
      {pmin}
      {pmax}
    />

    {#if frame.aeroVertices && frame.aeroIndices}
      <AeroMesh
        vertices={frame.aeroVertices}
        indices={frame.aeroIndices}
      />
    {/if}

    <AxisGizmo
      position={Array.from(frame.position) as [number, number, number]}
      rotation={Array.from(frame.rotation)}
      scale={1}
    />

    {#if showForces}
      <HydroForces
        faceCops={frame.faceCops}
        faceNormals={frame.faceNormals}
        facePressure={frame.facePressure}
      />
    {/if}
  {/if}
</T.Group>
