<!-- src/lib/HydroForces.svelte -->
<!--
  Renders one arrow per submerged face, at the centre of pressure,
  pointing along the outward normal scaled by hydrostatic pressure.

  `pressureScale` lets you tune visual length: length = pressure * pressureScale
-->
<script lang="ts">
  import { T } from '@threlte/core'
  import { BufferGeometry, BufferAttribute, LineSegments, LineBasicMaterial } from 'three'

  let {
    faceCops,
    faceNormals,
    facePressure,
    pressureScale = 0.00005,
    color         = 0x00ff88,
  }: {
    faceCops:      Float32Array
    faceNormals:   Float32Array
    facePressure:  Float32Array
    pressureScale?: number
    color?:         number
  } = $props()

  // Build a single LineSegments geometry — one segment per face (2 verts each).
  // Much cheaper than N individual Arrow components for many faces.
  let geo = $derived.by(() => {
    const faceCount = facePressure.length
    const positions = new Float32Array(faceCount * 6) // 2 verts * 3 coords

    for (let i = 0; i < faceCount; i++) {
      const ox = faceCops[i*3],     oy = faceCops[i*3+1],     oz = faceCops[i*3+2]
      const nx = faceNormals[i*3],  ny = faceNormals[i*3+1],  nz = faceNormals[i*3+2]
      const len = facePressure[i] * pressureScale

      positions[i*6]   = ox
      positions[i*6+1] = oy
      positions[i*6+2] = oz
      positions[i*6+3] = ox + nx * len
      positions[i*6+4] = oy + ny * len
      positions[i*6+5] = oz + nz * len
    }

    const g = new BufferGeometry()
    g.setAttribute('position', new BufferAttribute(positions, 3))
    return g
  })

  let mat = $derived(new LineBasicMaterial({ color }))

  $effect(() => {
    const g = geo
    return () => g.dispose()
  })
</script>

<T.LineSegments geometry={geo} material={mat} />