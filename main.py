from random import randrange
import platform,time,sys,json

def typingPrint(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  time.sleep(0.5)
  print("")
  
if platform.system() == "Linux" or platform.system() == "Darwin":
  slash = "/"
elif platform.system() == "Windows":
  slash = "\\"


def getModule(mod):
  f = open(f"CharlesDarwin.json", "r")
  j = json.loads(f.read())
  conections = j[f"module{mod}"]
  f.close()
  return conections

def editModules(mod, edit):
  f = open(f"CharlesDarwin.json", "r")
  j = json.loads(f.read())
  f.close()
  j[f"module{mod}"] = edit
  j = json.dumps(j, indent=2)
  f = open(f"CharlesDarwin.json", "w")
  f.write(j)
  f.close()
  
def deleteModule(mod):
  global modules
  f = open(f"CharlesDarwin.json", "r")
  j = json.loads(f.read())
  f.close()
  if f"module{mod}" in j:
    del j[f"module{mod}"]
    j = json.dumps(j, indent=2)
    f = open(f"CharlesDarwin.json", "w")
    f.write(j)
    f.close()
    modules -= 1
  else:
    typingPrint("The module does not exist")
    
def modulesGen(count):
  for i in range(1,count+1):
    if i == 1:
      a = 0
    else:
      a = i - 1
    if i == count:
      b = 0
    else:  
      b = i + 1
    if randrange(1,5) == 1 and count - i >= 10:
      c = randrange(i+2,i+10)
    else:
      c = 0
    if randrange(1,5) == 1 and i >= 11:
      d = randrange(i-10, i-2)
    else:
      d = 0
    editModules(i, f"{a} {b} {c} {d}")

modules = 100
modulesGen(modules)
start_module = 1
module = start_module
q_module = randrange(10,modules)
moves = getModule(module).split()

health = 10*modules
alive = True
ship_power = 40*modules
flame_ammo = round(modules/2)
won = False
vents = [] 
info_panels = []
workers = []

def setup():
  for i in range(randrange(2,round(modules/2))):
    vent = randrange(start_module+1,modules)
    while vent in vents:
      vent = randrange(start_module+1,modules)
    vents.append(vent)
  for i in range(randrange(2,round(modules/4))):
    panel = randrange(start_module+1,modules)
    while panel in info_panels:
      panel = randrange(start_module+1,modules)
    info_panels.append(panel)
  for i in range(randrange(2,round(modules/2))):
    workers.append(randrange(start_module+1,modules))

def get_action():
  global module, vents, info_panels, ship_power
  global workers, q_module, flame_ammo, won, health
  
  moves = getModule(module).split()
  typingPrint("Module: "+ str(module))
  typingPrint("Health: "+ str(health))
  typingPrint("Flamethrower Juice: "+ str(flame_ammo))
  typingPrint("Ship power: "+ str(ship_power))
  typingPrint("You can go to module(s):")
  
  for i in moves:
    if int(i) > 0:
      typingPrint(str(i))

  contents = []
  module = int(module)
  if module in vents:
     contents.append("-Vent (Other exits are blocked)")
  if module in info_panels:
    contents.append("-Info_panel (To locate the queen)")
  if module in workers:
    contents.append("-Worker (May kill if not killed)")
  if module == q_module:
    contents.append("-The Queen")
  if len(contents) > 0:
    typingPrint("Your room contains:")
    for i in contents:
      typingPrint(i+"\n")

  typingPrint("What do you want to do next ? (MOVE, VENT, SHOOT, INFO PANEL)")
  actions = ["MOVE", "VENT", "SHOOT", "INFO PANEL", "move", "vent", "shoot", "info panel"]
  action = input(">")
  if action in actions:
    if "MOVE" in action or "move" in action:
      typingPrint("Enter module to move to")
      inp = input(">")
      if inp in moves:
        module = inp
        ship_power -= 25
    elif "VENT" in action or "vent" in action:
      typingPrint("You are being moved elsewhere in the ship")
      module = randrange(start_module, modules)
      ship_power -= 50
    elif "SHOOT" in action or "shoot" in action:
      if module in workers:
        typingPrint("You aim for the worker")
        flame_ammo -= 1
        if randrange(0,6) > 0:
          typingPrint("You killed the worker doing it's job!")
          workers.remove(module)
        else:
          typingPrint("You missed and probably made a hole in the ship")
      elif module == q_module:
        typingPrint("You aim for the queen")
        flame_ammo -= 1
        if randrange(0,6) > 3:
          typingPrint("You killed the queen!")
          won = True
        else:
          typingPrint("You missed and probably made a hole in the ship")
    elif "INFO PANEL" in action or "info panel" in action:
      typingPrint("You read the Info Panel:")
      typingPrint("The Queen is in module"+str(q_module))
      ship_power -= 100
    else:
      typingPrint("Invalid Action")
    if module in workers:
        typingPrint("The workers aim for you")
        flame_ammo -= 1
        if randrange(0,6) <= 1:
          typingPrint("The workers shot you")
          health -= 25
        else:
          typingPrint("They missed you continue to survive")
    if module == q_module:
        typingPrint("The Queen aims for you")
        flame_ammo -= 1
        if randrange(0,6) <= 3:
          typingPrint("The workers shot you")
          health -= 35
        else:
          typingPrint("They missed you continue to survive")
  else:
    typingPrint("Invalid Action")

typingPrint("WELCOME TO:")
time.sleep(0.5)
typingPrint(
      """
████████╗███████╗██╗     ██╗██╗   ██╗███╗   ███╗
╚══██╔══╝██╔════╝██║     ██║██║   ██║████╗ ████║
   ██║   █████╗  ██║     ██║██║   ██║██╔████╔██║
   ██║   ██╔══╝  ██║     ██║██║   ██║██║╚██╔╝██║
   ██║   ███████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║
   ╚═╝   ╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝
""")

setup()
while alive:
  get_action()
  if health <= 0:
    alive = False 
    typingPrint("You died after sustaining too much damage")
  if ship_power <= 0:
    typingPrint("You died after the ship lost power sucking you out into space and leaving you a flash frozen corpse endlessly drifting in the void")
  if won:
    typingPrint("You won")
  print("\n")