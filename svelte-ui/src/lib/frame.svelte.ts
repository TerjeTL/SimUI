import type { Frame } from '../frame.ts'

export type { Frame }

export class FrameStore {
  frames  = $state<Frame[]>([])
  current = $state(0)

  get currentFrame(): Frame | null {
    return this.frames[this.current] ?? null
  }

  add(frame: Frame) {
    this.frames.push(frame)
  }

  clear() {
    this.frames  = []
    this.current = 0
  }
}
