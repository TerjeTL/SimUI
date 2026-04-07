from sim_ui import SimUI, Frame

ui = SimUI()  # generates vizdata.g.ts
ui.send(Frame(boxPosition=(-2, 1, 0)))
ui.show()

print("window closed")
