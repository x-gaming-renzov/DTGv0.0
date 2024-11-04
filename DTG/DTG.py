import json
from .classes.LLM import LLM
from .prompts import prompt_funcs
import time
from .classes.OutputClasses import Tree, PossibleEndings

def get_dialogue_json(input_info):
    t_0 = time.time()
    starting_time = time.time()
    performance_dict = {
        'tags' : 0,
        'abstract' : 0,
        'endings' : 0,
        'tree' : 0
    }
    llm = LLM()
    print(f'Generating tags.')
    tags_by_llm = llm.send_message_for_code(prompt_funcs.tag_prompt(input_info), model='gpt-4o-mini')
    print(f'Tags generated in {time.time() - starting_time} seconds.')
    performance_dict['tags'] = time.time() - starting_time
    starting_time = time.time()
    print(f'Generating abstract.')
    abstract = llm.send_message_for_code(prompt_funcs.abstract_prompt(tags_by_llm, input_info))
    print(f'Abstract generated in {time.time() - starting_time} seconds.')
    performance_dict['abstract'] = time.time() - starting_time
    starting_time = time.time()
    print(f'Generating possible endings.')
    endings_by_llm = llm.send_message_for_format(prompt_funcs.possible_ending_prompt(abstract), PossibleEndings ,model='gpt-4o')
    print(f'Possible endings generated in {time.time() - starting_time} seconds.')
    performance_dict['endings'] = time.time() - starting_time
    starting_time = time.time()
    print(f'Generating dialogue tree.')
    tree_by_llm = llm.send_message_for_format(prompt_funcs.dialogue_prompt(abstract, endings_by_llm, tags_by_llm), format=Tree,model='gpt-4o')
    print(f'Dialogue tree generated in {time.time() - starting_time} seconds.')
    performance_dict['tree'] = time.time() - starting_time
    starting_time = time.time()
    print(f'Total time taken : {time.time() - t_0} seconds.')
    print(f'Performance dict : {performance_dict}')
    #formatted_endings_json = json.loads(endings_by_llm)
    return tree_by_llm, endings_by_llm
