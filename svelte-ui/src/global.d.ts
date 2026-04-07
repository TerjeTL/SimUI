interface Window {
  onData: <K extends keyof import('./simdata').SimData>(
    key: K,
    value: import('./simdata').SimData[K]
  ) => void
}
