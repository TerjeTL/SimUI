import type { SimData } from '../simdata.ts'

export interface HullFrame {
  index:        number
  time?:        number

  // submerged mesh
  vertices:     Float32Array   // Nx3 flat
  indices:      Uint32Array    // Mx3 flat (triangles)

  // per-face hydrostatic data (one entry per triangle)
  faceNormals:  Float32Array   // Fx3 flat, outward world-space normals
  faceCops:     Float32Array   // Fx3 flat, centre of pressure world-space
  facePressure: Float32Array   // Fx1 flat, hydrostatic pressure magnitude (Pa)

  // entity transform
  position:     Float32Array   // 3
  rotation:     Float32Array   // 9, row-major 3x3

  // full hull wireframe (world-space) — optional
  hullVertices?: Float32Array  // Nx3 flat
  hullIndices?:  Uint32Array   // Mx3 flat

  // water surface wireframe (world-space) — optional
  waterVertices?: Float32Array // Nx3 flat
  waterIndices?:  Uint32Array  // Mx3 flat

  // above-water (aero) mesh — optional
  aeroVertices?: Float32Array  // Nx3 flat
  aeroIndices?:  Uint32Array   // Mx3 flat
}

/** Convert a complete SimData (JSON transport, number[]) to a HullFrame with typed arrays. */
export function fromSimData(d: SimData): HullFrame {
  return {
    index:        d.index,
    time:         d.time,
    vertices:     new Float32Array(d.vertices),
    indices:      new Uint32Array(d.indices),
    faceNormals:  new Float32Array(d.faceNormals),
    faceCops:     new Float32Array(d.faceCops),
    facePressure: new Float32Array(d.facePressure),
    position:     new Float32Array(d.position),
    rotation:     new Float32Array(d.rotation),
    hullVertices:  d.hullVertices  ? new Float32Array(d.hullVertices)  : undefined,
    hullIndices:   d.hullIndices   ? new Uint32Array(d.hullIndices)    : undefined,
    waterVertices: d.waterVertices ? new Float32Array(d.waterVertices) : undefined,
    waterIndices:  d.waterIndices  ? new Uint32Array(d.waterIndices)   : undefined,
    aeroVertices:  d.aeroVertices  ? new Float32Array(d.aeroVertices)  : undefined,
    aeroIndices:   d.aeroIndices   ? new Uint32Array(d.aeroIndices)    : undefined,
  }
}

/** Returns true once all required mesh fields are present in a partial SimData. */
export function isComplete(d: Partial<SimData>): d is SimData {
  return (
    d.vertices     !== undefined &&
    d.indices      !== undefined &&
    d.faceNormals  !== undefined &&
    d.faceCops     !== undefined &&
    d.facePressure !== undefined &&
    d.position     !== undefined &&
    d.rotation     !== undefined
  )
}

export class FrameStore {
  frames  = $state<HullFrame[]>([])
  current = $state(0)

  get currentFrame(): HullFrame | null {
    return this.frames[this.current] ?? null
  }

  add(frame: HullFrame) {
    this.frames.push(frame)
  }

  clear() {
    this.frames  = []
    this.current = 0
  }
}
