import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from DTG import DTG
from streamlit_flow.layouts import TreeLayout

if 'npc_mood_text_input' not in st.session_state:
    st.session_state['NPC Mood'] = 'happy'
if 'npc_personality_text_input' not in st.session_state:
    st.session_state['NPC Personality'] = 'friendly'
if 'npc_convo_additional_flavour_text_input' not in st.session_state:
    st.session_state['NPC Convo Additional Flavour'] = 'pickles, groves, and the like'

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
            data={'content': node['npc_dialogue']},
            draggable=True,
            style={'backgroundColor': '#00c04b'}
        )

        tree_nodes.append(npc_node)
        #check if there are no player choices
        if node.get('player_choices') is None:
            continue
        if node['player_choices'] == []:
            continue
        for player_choice in node['player_choices']:
            node = StreamlitFlowNode(
                id=f"{node['id']}_|_{player_choice['next_node']}",
                pos=(0, 0),
                data={'content': player_choice['player_dialogue_choice']},
                draggable=True
            )
            tree_nodes.append(node)

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

flow_state = StreamlitFlowState([], [])
new_state = streamlit_flow('fully_interactive_flow', 
                flow_state, # Start with an empty state, or with some pre-initialized state
                fit_view=True,
                show_controls=True,
                allow_new_edges=True,
                animate_new_edges=True,
                layout=TreeLayout("right"),
                enable_pane_menu=True,
                enable_edge_menu=True,
                enable_node_menu=True,
)

def generate():
    st.write(st.session_state)
    input_info = {
        'mood' : st.session_state.get('npc_mood_text_input'),
        'personality' : st.session_state.get('npc_personality_text_input'),
        'convo_additional_flavour' : st.session_state.get('npc_convo_additional_flavour_text_input')
    }
    dialogue_tree_json = DTG.get_dialogue_json(input_info)
    dialogue_tree_nodes, dialogue_tree_edges = process_json(dialogue_tree_json)
    if 'nodes' not in st.session_state.fully_interactive_flow:
        st.session_state.fully_interactive_flow.nodes = []
    if 'edges' not in st.session_state.fully_interactive_flow:
        st.session_state.fully_interactive_flow.edges = []
    st.session_state.fully_interactive_flow.nodes = dialogue_tree_nodes
    st.session_state.fully_interactive_flow.edges = dialogue_tree_edges
#add generate button and when every clicked run function
st.write(st.session_state)
generate_button = st.button("Generate", on_click=generate)

