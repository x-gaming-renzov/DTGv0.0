from pydantic import BaseModel

class Ending(BaseModel):
    parameter_tag: str
    value: str

class PossibleEndings(BaseModel):
    positive: Ending
    neutral: Ending
    negative: Ending

class Choice(BaseModel):
    player_dialogue_choice: str
    next_node: str

class Node(BaseModel):
    id: str
    npc_dialogue: str
    tag_of_node: str
    player_dialogue_choices: list[Choice]
    end_node_effect: str
    is_end_node: bool

class Tree(BaseModel):
    nodes: list[Node]