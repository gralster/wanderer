from blessed import Terminal

t = Terminal()

with t.location(50,50):
    print(t.on_blue("     "))
with t.location(50,50):
    print(""+""+""+"x")
