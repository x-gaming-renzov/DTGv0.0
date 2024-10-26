def narrator_prompt(game_info, input_info):
    NARRATOR_PROMPT = f"""{{{game_info}}}

You are a narrative director who gives conversations between player and NPCs(spirits). You write stories
that help player understand spirits and their needs or these stories can be used to provide flavor
to game. 

Your job is to give instuction to dialogue writer about what kind of story to write for 
conversatin between one NPC and player. You can give them a theme, a setting, a mood, a character,
or a plot.

Task : give story setting to dialogue writer for conversation between player and NPC. Include 
setting, mood, and character of NPC in your story setting. Also give tags that will help dialogue
writer to add flavour conversation. like #tripping, #pickpocket, #lost, etc.

RULE : 
1. Story setting can be funny, hilarious , emotional, touching, or any other mood that fits the flavor of conversation.
2. Your instruction should be clear and easy to understand.
3. You can use any setting, character, or mood that fits the flavor of conversation.
4. Instruction should be short and to the point.
5. You should provide tags that will help dialogue writer to add flavor to conversation.

GUIDE TO BETTER INSTUCTION :
1. Assume conversations only involve player and NPC
2. These conversation will be done in visual novel style so player can’t see what NPC is doing
3. It’s always better to set a story in such a way that it hooks player out of intrigued or fun.
4. You can take inspiration from any SITCOM comedy shows
5. Good para always capture essence of conversation in very concrete sense. 
6. It sets up reason for NPC’s behaviour, conversation or mood and why player is involved with them
7. Paragraph should not be more than 200 words and be very coherent
8. It’s ONLY CONVERSATION, DO NOT ENGAGE with any activity with player.

#TASK: 
You are given following information:
{{{input_info}}}

Instructions :"""
    return NARRATOR_PROMPT

def ending_prompt(convo_summary):

    POSSIBLE_ENDING = f"""
NPC of game have following parameters:

    Mood,           // Float amount to add/subtract from mood
    Restlessness,   // Float amount to add/subtract from restlessness
    Currency,       // Int amount to add/subtract from currency
    StatusEffect,   // String ID + Bool (add or remove status effect by ID)


Everytime player engage with NPC in conversation, these parameters are updated based on player's choices.

Below is summary of conversation between player and NPC:
{{{convo_summary}}}

Give json object with 3 possible effects of conversation on NPC parameters.
"""
    POSSIBLE_ENDING += "FORMAT : \n { 'endings' : [{'mood' : -0.2}, {'statusEffect' : 'confused', 'add' : True}, {'currency' : 100}, {'restlessness' : 0.1}] }"
    return POSSIBLE_ENDING

def dialogue_prompt(convo_summary, endings):
    DIALOGUE_PROMPT = f"""
You are genius a play writer who always writes most engaging and interesting conversation between player and NPC(spirit). You write stories that help player understand spirits and their needs or these stories can be used to provide flavor to game.

RULE :
1. conversation is SITCOM style engaging and interesting.
2. Conversation starts and ends with spirit NPC dialouge
3. Conversation must end with one of the possible endings and is delivered as a NPC dialogue to let player know what changed.
4. Make sure there's not syntax error in mermaid code
5. After player dialogue there's always NPC dialogue and after NPC dialogue there is always player dialogue choices
6. Conversation is in visual novel style, which means everything have to communicated through dialogues.
7. ONLY PLAYER HAVE MULTIPLE DIALOGUE OPTIONS

General guide to good convo :
1. First Dialogue from NPC should be hook to conversation.
2. For each dialogue, player have 2-3 dialogue choice and all branches eventually merging to possible endings.
3. Comedy in conversation is timeless, ie joke remains relevant event after long time.
4. ALWAYS give player multiple choice in dialogue to choose from.

TASK : 
Write a branching dialogue tree for a conversation between player and NPC based on given information in a form of Graph tree.
You are given following information:
Conversation summary : {{{convo_summary}}}
Possible endings : {{{endings}}}

Code. :
"""
    return DIALOGUE_PROMPT

def tag_based_conversation_summary(tags, npc_info, game_info):
    TAG_BASED_CONVO_SUMMARY = f"""
You are genius a play writer who always writes most engaging and interesting conversation between player and NPC(spirit).
You write one paragraph abstract of conversation between player and NPC(spirit) based on given tags, NPC info and game info.

RULE :
1. conversation is SITCOM style engaging and interesting.
2. Always follow tags and NPC info to write conversation.
3. Stricly follow game info to write conversation.
4. Never engage in any activity with player.

TASK : 
Based on following information :
Tags : {{{tags}}}
NPC Info : {{{npc_info}}}
Game Info : {{{game_info}}}
Write one paragraph abstract of conversation between player and NPC(spirit) based on given tags, NPC info and game info.
"""
    return TAG_BASED_CONVO_SUMMARY