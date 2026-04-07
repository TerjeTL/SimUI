<script lang="ts">
  import type { SimData } from './simdata.ts'
  import { Canvas, T } from '@threlte/core'
  import { OrbitControls } from '@threlte/extras'

  let data = $state<Partial<SimData>>({})

  window.onData = (key, value) => {
    data[key] = value
  }
</script>

<Canvas>
  <T.PerspectiveCamera makeDefault position={[0, 2, 5]}>
    <OrbitControls enableDamping />
  </T.PerspectiveCamera>
  <T.DirectionalLight position={[5, 5, 5]} />
  <T.AmbientLight intensity={0.4} />
  <T.Mesh position={data.boxPosition ?? [0, 0, 0]}>
    <T.BoxGeometry />
    <T.MeshStandardMaterial color="hotpink" />
  </T.Mesh>
</Canvas>

<style>
  :global(body) { margin: 0; }
  :global(canvas) { display: block; width: 100vw; height: 100vh; }
</style>