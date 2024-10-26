import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from DTG import DTG
from streamlit_flow.layouts import TreeLayout
import json


st.write(st.session_state)
if 'curr_state' not in st.session_state:
    nodes = []

    edges = []

    st.session_state.curr_state = StreamlitFlowState(nodes, edges)

npc_mood_text_input = st.text_input("NPC Mood", "happy", key='npc_mood_text_input')
npc_personality_text_input = st.text_input("NPC Personality", "friendly", key='npc_personality_text_input')
npc_convo_additional_flavour_text_input = st.text_input("NPC Convo Additional Flavour", "pickles, groves, and the like", key='npc_convo_additional_flavour_text_input')

def process_json(json_data):
    tree_nodes = []
    tree_edges = []
    dt_nodes_from_json = json_data['nodes']
    for node in dt_nodes_from_json:
        npc_node = StreamlitFlowNode(
            id=node['id'],
            pos=(0,0),
            data={'content': 'NPC : ' + node['npc_dialogue']},
            draggable=True
        )

        tree_nodes.append(npc_node)
        #check if there are no player choices
        if node.get('player_dialogue_choices') is None:
            print('No player dialogue choices')
            continue
        if node['player_dialogue_choices'] == []:
            print('No player dialogue choices')
            continue

        for player_choice in node['player_dialogue_choices']:
            player_choice_node = StreamlitFlowNode(
                id=f"{node['id']}_|_{player_choice['next_node']}",
                pos=(0, 0),
                data={'content': 'Player : ' + player_choice['player_dialogue_choice']},
                draggable=True
            )
            tree_nodes.append(player_choice_node)

            pe_id = f'{node["id"]}_e_{node['id']}_|_{player_choice['next_node']}'
            pe_source = node['id']   
            pe_target = f"{node['id']}_|_{player_choice['next_node']}"
            p_edge = StreamlitFlowEdge(id=pe_id, source=pe_source, target=pe_target)

            ne_id = player_choice['next_node']
            ne_source = f"{node['id']}_|_{player_choice['next_node']}"
            ne_target = player_choice['next_node']
            n_edge = StreamlitFlowEdge(id=ne_id, source=ne_source, target=ne_target)

            tree_edges.append(p_edge)
            tree_edges.append(n_edge)
    return tree_nodes, tree_edges


if st.button("Generate"):
    input_info = {
        'mood' : st.session_state.get('npc_mood_text_input'),
        'personality' : st.session_state.get('npc_personality_text_input'),
        'convo_additional_flavour' : st.session_state.get('npc_convo_additional_flavour_text_input')
    }
    dialogue_tree_json = DTG.get_dialogue_json(input_info)
    with open('dialogue_tree.json', 'w') as f:
        f.write(json.dumps(dialogue_tree_json, indent=4))
    dialogue_tree_nodes, dialogue_tree_edges = process_json(dialogue_tree_json)
    print(type(dialogue_tree_nodes  ))
    print(type(dialogue_tree_edges))
    print(type (st.session_state.curr_state))
    st.session_state.curr_state.nodes = [node for node in st.session_state.curr_state.nodes if node.id not in [node.id for node in dialogue_tree_nodes]]
    st.session_state.curr_state.edges = [edge for edge in st.session_state.curr_state.edges if edge.id not in [edge.id for edge in dialogue_tree_edges]]
    st.rerun()

st.session_state.curr_state = streamlit_flow('example_flow', 
                                st.session_state.curr_state, 
                                layout=TreeLayout(direction='right'), 
                                fit_view=True, 
                                height=500, 
                                enable_node_menu=True,
                                enable_edge_menu=True,
                                enable_pane_menu=True,
                                get_edge_on_click=True,
                                get_node_on_click=True, 
                                show_minimap=True, 
                                hide_watermark=True, 
                                allow_new_edges=True,
                                min_zoom=0.1)
