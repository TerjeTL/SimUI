<!-- src/lib/AxisGizmo.svelte -->
<!--
  Draws X (red), Y (green), Z (blue) axes at the given position/rotation.
  `rotation` is a flat row-major 3x3 Float32Array or number[9].
  `scale` controls axis line length.
-->
<script lang="ts">
  import { T } from '@threlte/core'
  import Arrow from './Arrow.svelte'
  import { Matrix4, Euler } from 'three'

  let {
    position = [0, 0, 0],
    rotation = [1,0,0, 0,1,0, 0,0,1],
    scale    = 1.0,
  }: {
    position?: [number, number, number] | Float32Array
    rotation?: Float32Array | number[]
    scale?:    number
  } = $props()

  // extract column vectors of the rotation matrix (= local axes in world space)
  let axes = $derived.by(() => {
    const r = rotation
    return {
      x: [r[0] * scale, r[3] * scale, r[6] * scale] as [number,number,number],
      y: [r[1] * scale, r[4] * scale, r[7] * scale] as [number,number,number],
      z: [r[2] * scale, r[5] * scale, r[8] * scale] as [number,number,number],
    }
  })

  let pos = $derived([position[0], position[1], position[2]] as [number,number,number])
</script>

<Arrow origin={pos} dir={axes.x} color={0xff2222} />
<Arrow origin={pos} dir={axes.y} color={0x22ff22} />
<Arrow origin={pos} dir={axes.z} color={0x2222ff} />