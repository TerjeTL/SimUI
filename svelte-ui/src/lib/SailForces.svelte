<!-- src/lib/SailForces.svelte -->
<!-- Renders one arrow per sail strip at the quarter-chord cp, scaled by forceScale. -->
<script lang="ts">
  import { T } from '@threlte/core'
  import { BufferGeometry, BufferAttribute, LineSegments, LineBasicMaterial } from 'three'

  let {
    origins,
    vectors,
    forceScale = 0.01,
    color      = 0xff6600,
  }: {
    origins:      Float32Array
    vectors:      Float32Array
    forceScale?:  number
    color?:       number
  } = $props()

  let geo = $derived.by(() => {
    const n         = origins.length / 3
    const positions = new Float32Array(n * 6)

    for (let i = 0; i < n; i++) {
      const ox = origins[i*3],   oy = origins[i*3+1], oz = origins[i*3+2]
      const fx = vectors[i*3],   fy = vectors[i*3+1], fz = vectors[i*3+2]
      positions[i*6]   = ox
      positions[i*6+1] = oy
      positions[i*6+2] = oz
      positions[i*6+3] = ox + fx * forceScale
      positions[i*6+4] = oy + fy * forceScale
      positions[i*6+5] = oz + fz * forceScale
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
