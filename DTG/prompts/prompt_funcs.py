#tags category for types of flavour in conversation between player and NPC
tags_categories = ['greeting', 'goodbye', 'question', 'answer', 'statement', 'exclamation', 'apology', 'thanks', 'compliment', 'insult', 'encouragement', 'disagreement', 'agreement', 'disappointment', 'sympathy', 'praise', 'criticism', 'joke', 'story', 'advice', 'request', 'offer', 'suggestion', 'warning', 'funny', 'serious', 'sad', 'happy', 'angry', 'scared', 'surprised', 'disgusted', 'confused', 'excited', 'bored', 'tired', 'calm', 'relaxed', 'energetic', 'friendly', 'unfriendly', 'polite', 'rude', 'formal', 'informal', 'positive', 'negative', 'neutral', 'open', 'closed', 'direct', 'indirect', 'honest', 'dishonest', 'confident', 'insecure', 'optimistic', 'pessimistic', 'patient', 'impatient', 'kind', 'mean', 'generous', 'selfish', 'humble', 'arrogant', 'sincere', 'insincere', 'intelligent', 'stupid', 'creative', 'uncreative', 'sensible', 'nonsensical', 'logical', 'illogical', 'reasonable', 'unreasonable', 'practical', 'impractical', 'realistic', 'unrealistic', 'flexible', 'rigid', 'organized', 'disorganized', 'efficient', 'inefficient', 'responsible', 'irresponsible', 'reliable', 'unreliable', 'trustworthy', 'untrustworthy', 'loyal', 'disloyal', 'cooperative', 'uncooperative', 'helpful', 'unhelpful', 'supportive', 'unsupportive', 'understanding', 'ununderstanding', 'tolerant', 'intolerant', 'patient', 'impatient', 'forgiving', 'unforgiving', 'sympathetic', 'unsympathetic', 'empathetic', 'unempathetic', 'compassionate', 'uncompassionate', 'friendly', 'unfriendly', 'sociable', 'unsociable', 'outgoing', 'shy', 'confident', 'insecure', 'optimistic', 'pessimistic', 'cheerful', 'gloomy', 'happy', 'sad', 'excited', 'bored', 'relaxed', 'tense', 'calm', 'nervous', 'energetic', 'tired', 'friendly', 'unfriendly', 'polite', 'rude', 'formal', 'informal', 'positive', 'negative', 'neutral']

ABOUT_GAME = """
Game is management sim where player takes role of a manager of spirit concourse where spirits come
before moving on to afterlife. Player must manage spirits, keep them happy, and help them move on 
by providing them facilities and services. Player must also manage the concourse itself, building 
new facilities, hiring staff, and keeping the concourse running smoothly. Game is played in real-time
and player must make decisions quickly to keep spirits happy and concourse running smoothly.

Role of player : Manager of spirit concourse
Role of spirits : Spirits come to concourse before moving on to afterlife. They have needs and desires
written in their fulfillment plan.

Facilities : Buildings that provide services to spirits. Facilities can be built, upgraded, and destroyed.
Some facilities are - arcade, library, garden, bar, spa, dance floor, seance room, etc."""


def tag_prompt(INPUT_INFO):
    TAG_PROMPT = f"""
You are a helpful assistant that generates tags for branching dialogues tree of conversation between NPC and player in a video game.

You assign 3-5 tags to build a dialohue tree from following tag categories: {', '.join(tags_categories)}

RULES:
1. Tags should be in format of #tag1 #tag2 #tag3
2. Tags should be separated by space
3. Tags should be related to conversation between NPC and player
4. DO NOT include any irrelevant tags
5. Only include tags that are in the list of tag categories

About the game : {ABOUT_GAME}

About NPC : {INPUT_INFO}

Tags for branching dialogue tree :
"""
    return TAG_PROMPT

def abstract_prompt(tags_by_llm, INPUT_INFO):
    ABSTRACT_PROMPT = f"""
You are genius a play writer who always writes most engaging and interesting conversation between player and NPC(spirit).
You write one paragraph abstract of conversation between player and NPC(spirit) based on given tags, NPC info and game info.

RULE :
1. conversation is SITCOM style engaging and interesting.
2. Always follow tags and NPC info to write conversation.
3. Stricly follow game info to write conversation.
4. Never engage in any activity with player.
5. Never give exact dialogue, just write abstract of conversation.

TASK : 
Based on following information :
Tags : {{{tags_by_llm}}}
NPC Info : {{{INPUT_INFO}}}
Game Info : {{{ABOUT_GAME}}}
Write one paragraph abstract of conversation between player and NPC(spirit) based on given tags, NPC info and game info.
"""
    return ABSTRACT_PROMPT
    
def possible_ending_prompt(abstract):
    POSSIBLE_ENDINGS_PROMPT = f"""NPC of game have following parameters:
Parameter_tags :
    Mood,           // Float amount to add/subtract from mood
    Restlessness,   // Float amount to add/subtract from restlessness
    Currency,       // Int amount to add/subtract from currency
    StatusEffect,   // String ID + Bool (add or remove status effect by ID)


Everytime player engage with NPC in conversation, these parameters are updated based on player's choices.

RULES : 
1. Endings must be balanced and should not be too much in favor of player.
2. There must be always one negative ending.
3. There must be always one neutral ending.
4. There must be always one positive ending.
5. Ending parameters must be realistic and not too extreme.
6. Ending parameters must be balanced and not too much in favor of player.
7. Ending parameters must be balanced and not too much in favor of NPC.
8. Ending parameters must be balanced and not too much in favor of game world.
9. Strictly follow answer format.

Below is summary of conversation between player and NPC:
{{{abstract}}}

Give json object with 3 possible effects of conversation on NPC parameters.
json format:
{{
    "endings" : [
        {{"mood" : -0.2}},
        {{"statusEffect" : "confused", "add" : True}},
        {{"currency" : 100}},
        {{"restlessness" : 0.1}}
    ]
}}
"""
    return POSSIBLE_ENDINGS_PROMPT

def dialogue_prompt(abstract, endings_by_llm, tags_by_llm):
    DIALOGUE_TREE_PROMPT = f"""
Game Context: {ABOUT_GAME}

You are genius a play writer who always writes most engaging and interesting conversation between player and NPC(spirit). You write stories that help player understand spirits and their needs or these stories can be used to provide flavor to game.

RULE :
1. conversation is SITCOM style engaging and interesting.
2. Conversation starts and ends with spirit NPC dialouge
3. Conversation must lead to one of the end with the possible endings and is delivered as a NPC dialogue to let player know what changed.
4. Make sure there's not syntax error in mermaid code
5. There should never be any consecutive player dialogue, always NPC dialogue after player dialogue.
6. Conversation is in visual novel style, which means everything have to communicated through dialogues.
7. ONLY PLAYER HAVE MULTIPLE DIALOGUE OPTIONS, ALWAYS give player multiple choice in dialogue to choose from.
8. Tree always spread and ends with possible endings.
9. There is ONLY ONE ENDING for node. 
10. Tree MUST end in tree nodes with each ending

General guide to good convo :
1. First Dialogue from NPC should be hook to conversation.
2. For each dialogue, player have 2-3 dialogue choice and all branches eventually merging to possible endings.
3. Comedy in conversation is timeless, ie joke remains relevant event after long time.
4. Depth in conversation is important, it should not be shallow.
5. ALWAYS give player multiple choice in dialogue to choose from.
6. Size of tree should be at least 3 levels deep.

TASK : 
Write a branching dialogue tree for a conversation between player and NPC based on given information in a form of Graph tree and return it json string. 
You are given following information:
Conversation summary : {{{abstract}}}
Possible endings : {{{endings_by_llm}}}
Tags for branching dialogue tree : {{{tags_by_llm}}}

FORMAT : `
{{
    'nodes' : [
        {{
            'id' : 'unique string id of node',
            'npc_dialogue' : 'npc dialogue in string. this is what NPC says to player',
            'tag_of_node' : 'unique tag of node describing this stage of conversation',
            'player_dialogue_choices' : [
                {{
                    'player_dialogue_choice' : 'dialogue option 1 for player. this is what player says to NPC',
                    'next_node' : 'unique string id of next node'
                }},
                {{
                    'player_dialogue_choice' : 'dialogue option 2 for player. this is what player says to NPC',
                    'next_node' : 'unique string id of next node'
                }}
            ],
            'end_node_effect' : positive/negative/neutral,
            'is_end_node' : false/true
        }},
        {{
            'id' : 'unique string id of node',
            'npc_dialogue' : 'npc dialogue',
            'tag_of_node' : 'unique tag of node describing this stage of conversation',
            'player_dialogue_choices' : [
                {{
                    'player_dialogue_choice' : 'dialogue option 1 for player in string',
                    'next_node' : 'unique string id of next node in string'
                }},
                {{
                    'player_dialogue_choice' : 'dialogue option 2 for player',
                    'next_node' : 'unique string id of next node'
                }}
            ],
            'end_node_effect' : positive/negative/neutral,
            'is_end_node' : false/true
        }},...
    ]
}}`
"""
    return DIALOGUE_TREE_PROMPT
    
def format_prompt(code):
    FORMATING_PROMPT = f"""
Context : 
Node is a one round in conversation where NPC says a dialogue and player have multiple dialogue choices to choose from.
One node can have multiple player dialogue choices and each choice leads to different next node.
Node always have id, npc_dialogue, tag_of_node, player_dialogue_choices, endtag (only for ending node)


About the task :
You read mermaid code for dialogue tree and now you have to convert it into json format for game engine to understand and implement it in game.
Remember, code can be in any format, ie mermaid, json, xml, etc. But output must be in json format.

Code : {code}

RULE : 
1. Always give json format.
2. Give tag to each node.
3. Always give player dialogue choices and next node for each player dialogue choice.
4. Player dialogue choice must be what player says to NPC.
5. Node always have id, npc_dialogue, tag_of_node, player_dialogue_choices, endtag (only for ending node)
6. npc_dialogue is what NPC says to player.

Format : 
{{
    'nodes' : [
        {{
            'id' : 'unique string id of node',
            'npc_dialogue' : 'npc dialogue in string. this is what NPC says to player',
            'tag_of_node' : 'unique tag of node describing this stage of conversation',
            'player_dialogue_choices' : [
                {{
                    'player_dialogue_choice' : 'dialogue option 1 for player. this is what player says to NPC',
                    'next_node' : 'unique string id of next node'
                }},
                {{
                    'player_dialogue_choice' : 'dialogue option 2 for player. this is what player says to NPC',
                    'next_node' : 'unique string id of next node'
                }}
            ],
            'end_node_effect' : {{ending dict from possible endings for possible ending node (only for ending node)}}
        }},
        {{
            'id' : 'unique string id of node',
            'npc_dialogue' : 'npc dialogue',
            'tag_of_node' : 'unique tag of node describing this stage of conversation',
            'player_dialogue_choices' : [
                {{
                    'player_dialogue_choice' : 'dialogue option 1 for player in string',
                    'next_node' : 'unique string id of next node in string'
                }},
                {{
                    'player_dialogue_choice' : 'dialogue option 2 for player',
                    'next_node' : 'unique string id of next node'
                }}
            ],
            'end_node_effect' : {{ending dict from possible endings for possible ending node (only for ending node)}}
        }},...
    ]
}}
"""
    return FORMATING_PROMPT

def regenrate_node_prompt(node_id, tree, instruction=None):
    REGENRATE_PROMPT = f"""
Context : 
About Game : {ABOUT_GAME}

You are genius play writer. You have written below dialogue tree for a game but user wants you to regenerate it. 

Tree : {tree}

#Task :
Regenrate following node : 
Node id to regenerate : {node_id}
Instructions by user : {instruction}

RULES : 
1. Do not break consistency and flow of conversation.
2. ONLY change node that user asked you to.
3. Do not halucinate. 
"""