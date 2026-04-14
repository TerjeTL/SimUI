<!-- src/lib/SubmergedMesh.svelte -->
<script lang="ts">
  import { T } from '@threlte/core'
  import { BufferGeometry, BufferAttribute, DoubleSide } from 'three'
  import { LUT } from './colormap.ts'

  let {
    vertices,
    indices,
    facePressure,
    pmin,
    pmax,
    color       = 0x888888,
    opacity     = 1.0,
    polygonOffset       = false,
    polygonOffsetFactor = 0,
    polygonOffsetUnits  = 0,
  }: {
    vertices:      Float32Array
    indices:       Uint32Array
    facePressure?: Float32Array
    pmin?:         number
    pmax?:         number
    color?:        number
    opacity?:      number
    polygonOffset?:       boolean
    polygonOffsetFactor?: number
    polygonOffsetUnits?:  number
  } = $props()

  let geo = $derived.by(() => {
    const g = new BufferGeometry()
    g.setAttribute('position', new BufferAttribute(vertices, 3))
    g.setIndex(new BufferAttribute(indices, 1))

    if (facePressure && facePressure.length > 0) {
      const faceCount = facePressure.length
      const mn    = pmin ?? 0
      const range = (pmax ?? mn) - mn || 1

      const colors = new Float32Array(faceCount * 9)
      for (let i = 0; i < faceCount; i++) {
        const idx = Math.round(Math.max(0, Math.min(1, (facePressure[i] - mn) / range)) * 255) * 3
        const r = LUT[idx], gr = LUT[idx+1], b = LUT[idx+2]
        for (let v = 0; v < 3; v++) {
          colors[(i*3+v)*3]   = r
          colors[(i*3+v)*3+1] = gr
          colors[(i*3+v)*3+2] = b
        }
      }
      g.setAttribute('color', new BufferAttribute(colors, 3))
    }

    return g
  })

  $effect(() => {
    const g = geo
    return () => g.dispose()
  })
</script>

{#if facePressure && facePressure.length > 0}
  <T.Mesh geometry={geo}>
    <T.MeshLambertMaterial
      vertexColors
      flatShading
      side={DoubleSide}
      {polygonOffset}
      {polygonOffsetFactor}
      {polygonOffsetUnits}
    />
  </T.Mesh>
{:else}
  <T.Mesh geometry={geo}>
    <T.MeshLambertMaterial
      {color}
      side={DoubleSide}
      transparent={opacity < 1}
      {opacity}
      {polygonOffset}
      {polygonOffsetFactor}
      {polygonOffsetUnits}
    />
  </T.Mesh>
{/if}
