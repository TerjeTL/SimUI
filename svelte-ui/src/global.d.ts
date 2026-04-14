import type { EncodedFrame } from './frame.ts'

declare global {
  interface Window {
    onFrame: (frame: EncodedFrame) => void
  }
}
