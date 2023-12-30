import mesa

from agents import FireAgent, FireFighterAgent
from model import FireControllerAgentModel

def agents_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is FireAgent:
        if agent.state == 0:
            portrayal["Color"] = "green"
            portrayal["Shape"] = "rect"
            portrayal["Filled"] = "true"
            portrayal["Layer"] = 0
            portrayal["w"] = 1
            portrayal["h"] = 1
        elif agent.state == 1:
            portrayal["Color"] = "yellow"
            portrayal["Shape"] = "rect"
            portrayal["Filled"] = "true"
            portrayal["Layer"] = 0
            portrayal["w"] = 1
            portrayal["h"] = 1
        elif agent.state == 2:
            portrayal["Color"] = "#FFCE33"
            portrayal["Shape"] = "rect"
            portrayal["Filled"] = "true"
            portrayal["Layer"] = 0
            portrayal["w"] = 1
            portrayal["h"] = 1
        elif agent.state == 3:
            portrayal["Color"] = "#FF9933"
            portrayal["Shape"] = "rect"
            portrayal["Filled"] = "true"
            portrayal["Layer"] = 0
            portrayal["w"] = 1
            portrayal["h"] = 1
        elif agent.state == 4:
            portrayal["Color"] = "red"
            portrayal["Shape"] = "rect"
            portrayal["Filled"] = "true"
            portrayal["Layer"] = 0
            portrayal["w"] = 1
            portrayal["h"] = 1
        elif agent.state == 5:
            portrayal["Color"] = "black"
            portrayal["Shape"] = "rect"
            portrayal["Filled"] = "true"
            portrayal["Layer"] = 0
            portrayal["w"] = 1
            portrayal["h"] = 1
    elif type(agent) is FireFighterAgent:
        portrayal["Color"] = "blue"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

model_params = {
    "width": 10,
    "height": 10, 
    "fire_fighters": 1,
    "fire_agents_values": [1,2,3]
}

grid = mesa.visualization.CanvasGrid(agents_portrayal, 10, 10, 500, 500)

server = mesa.visualization.ModularServer(
    FireControllerAgentModel, [grid], "Fire forest - model", model_params)
server.port = 8521
server.launch()