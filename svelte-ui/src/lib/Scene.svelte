<!-- src/lib/Scene.svelte -->
<script lang="ts">
  import { T } from '@threlte/core'
  import { OrbitControls } from '@threlte/extras'
  import type { OrbitControls as ThreeOrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
  import type { Frame } from './frame.svelte.ts'
  import SubmergedMesh from '$lib/SubmergedMesh.svelte'
  import AeroMesh      from '$lib/AeroMesh.svelte'
  import WireframeMesh from '$lib/WireframeMesh.svelte'
  import HydroForces   from '$lib/HydroForces.svelte'
  import AxisGizmo     from '$lib/AxisGizmo.svelte'
  import RigLine       from '$lib/RigLine.svelte'
  import Sail          from '$lib/Sail.svelte'
  import SailForces    from '$lib/SailForces.svelte'
  let {
    frame,
    pmin,
    pmax,
    showForces = true,
  }: {
    frame:       Frame | null
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

    {#if frame.waterVertices && frame.waterIndices}
      <WireframeMesh
        vertices={frame.waterVertices}
        indices={frame.waterIndices}
        color={0x1a8cff}
        opacity={0.35}
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

    {#if frame.mastPoints}
      <RigLine
        a={[frame.mastPoints[0], frame.mastPoints[1], frame.mastPoints[2]]}
        b={[frame.mastPoints[3], frame.mastPoints[4], frame.mastPoints[5]]}
        color={0xcccccc}
      />
    {/if}

    {#if frame.boomPoints}
      <RigLine
        a={[frame.boomPoints[0], frame.boomPoints[1], frame.boomPoints[2]]}
        b={[frame.boomPoints[3], frame.boomPoints[4], frame.boomPoints[5]]}
        color={0xaaaaaa}
      />
    {/if}

    {#if frame.sailStripVertices && frame.sailStripIndices}
      <Sail
        vertices={frame.sailStripVertices}
        indices={frame.sailStripIndices}
      />
    {/if}

    {#if frame.sailForceOrigins && frame.sailForceVectors}
      <SailForces
        origins={frame.sailForceOrigins}
        vectors={frame.sailForceVectors}
      />
    {/if}

    {#if frame.foilStripVertices && frame.foilStripIndices}
      <Sail
        vertices={frame.foilStripVertices}
        indices={frame.foilStripIndices}
        color={0x3a7bd5}
        opacity={0.85}
      />
    {/if}

    {#if frame.foilForceOrigins && frame.foilForceVectors}
      <SailForces
        origins={frame.foilForceOrigins}
        vectors={frame.foilForceVectors}
        color={0x00ccff}
        forceScale={0.005}
      />
    {/if}
  {/if}
</T.Group>
