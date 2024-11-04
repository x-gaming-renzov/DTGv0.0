from flask import Flask, request, jsonify
from DTG.DTG import get_dialogue_json
from DTG.classes.LLM import LLM
from DTG.prompts import prompt_funcs
from DTG.classes.OutputClasses import *

app = Flask(__name__)

@app.route('/generate_tags', methods=['POST'])
def generate_tags():
    data = request.json
    print(data)
    input_info = data.get('input_info')
    llm = LLM()
    tags_by_llm = llm.send_message_for_code(prompt_funcs.tag_prompt(input_info), model='gpt-4o-mini')
    return jsonify({'tags': tags_by_llm})

@app.route('/generate_abstract', methods=['POST'])
def generate_abstract():
    data = request.json
    input_info = data.get('input_info')
    tags_by_llm = data.get('tags')
    llm = LLM()
    abstract = llm.send_message_for_code(prompt_funcs.abstract_prompt(tags_by_llm, input_info))
    return jsonify({'abstract': abstract})

@app.route('/generate_possible_endings', methods=['POST'])
def generate_possible_endings():
    data = request.json
    abstract = data.get('abstract')
    llm = LLM()
    endings_by_llm = llm.send_message_for_format(prompt_funcs.possible_ending_prompt(abstract), PossibleEndings ,model='gpt-4o')
    return jsonify({'endings': endings_by_llm})

@app.route('/generate_dialogue_tree', methods=['POST'])
def generate_dialogue_tree():
    data = request.json
    abstract = data.get('abstract')
    endings_by_llm = data.get('endings')
    tags_by_llm = data.get('tags')
    llm = LLM()
    tree_by_llm = llm.send_message_for_format(prompt_funcs.dialogue_prompt(abstract, endings_by_llm, tags_by_llm), format=Tree, model='gpt-4o')
    return jsonify({'tree': tree_by_llm})

@app.route('/regenerate_prompt', methods=['POST'])
def generate_dialogue_tree():
    data = request.json
    node_id = data.get('node_id')
    tree = data.get('tree')
    instruction = data.get('instruction')
    llm = LLM()
    node = llm.send_message_for_format(prompt_funcs.regenrate_node_prompt(node_id=node_id, tree=tree, instruction=instruction), format=Node, model='gpt-4o')
    return jsonify({'node': node})

if __name__ == '__main__':
    app.run(debug=True)

