// Pre-baked LUT from d3-scale-chromatic — strings parsed once at module load,
// runtime access is pure Float32Array indexing.
import { interpolateGreens } from 'd3-scale-chromatic'
import { Color } from 'three'

const N   = 256
export const LUT = new Float32Array(N * 3)

const _c = new Color()
for (let i = 0; i < N; i++) {
  _c.set(interpolateGreens(i / (N - 1)))
  LUT[i*3]   = _c.r
  LUT[i*3+1] = _c.g
  LUT[i*3+2] = _c.b
}

/** Map normalised t ∈ [0,1] → [r, g, b] floats via the LUT. */
export function lutRGB(t: number): [number, number, number] {
  const i = Math.round(Math.max(0, Math.min(1, t)) * (N - 1)) * 3
  return [LUT[i], LUT[i+1], LUT[i+2]]
}

/** CSS rgb() string for a given t — used for CSS gradients. */
export function lutCSS(t: number): string {
  const [r, g, b] = lutRGB(t)
  return `rgb(${Math.round(r*255)},${Math.round(g*255)},${Math.round(b*255)})`
}
