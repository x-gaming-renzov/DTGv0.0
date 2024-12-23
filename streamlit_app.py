import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from DTG import DTG
from streamlit_flow.layouts import TreeLayout

if st.session_state.get('curr_state') is None:
    st.session_state.curr_state = StreamlitFlowState([], [])

def process_json(json_data):
    tree_nodes = []
    tree_edges = []
    try:
        dt_nodes_from_json = json_data['nodes']
        for i, node in enumerate(dt_nodes_from_json):
            npc_node = StreamlitFlowNode(
                id=node['id'],
                pos=(0,0),  # Space out nodes horizontally
                data={'content': 'NPC : ' + node['npc_dialogue']},
                draggable=True,
                node_type='default',
                source_position='right',
                target_position='left'
            )
            tree_nodes.append(npc_node)

            player_choices = node.get('player_dialogue_choices', [])
            for player_choice in enumerate(player_choices):
                player_choice_node = StreamlitFlowNode(
                    id=f"{node['id']}_{player_choice['next_node']}",
                    pos=(0,0),  # Position player choices vertically
                    data={'content': 'Player : ' + player_choice['player_dialogue_choice']},
                    draggable=True,
                    node_type='default',
                    source_position='right',
                    target_position='left'
                )
                tree_nodes.append(player_choice_node)

                p_edge = StreamlitFlowEdge(
                    id=f"{node['id']}_to_{player_choice_node.id}", 
                    source=node['id'],   
                    target=player_choice_node.id
                )
                n_edge = StreamlitFlowEdge(
                    id=f"{player_choice_node.id}_to_{player_choice['next_node']}",
                    source=player_choice_node.id,
                    target=player_choice['next_node']
                )
                tree_edges.append(p_edge)
                tree_edges.append(n_edge)

    except (KeyError, TypeError) as e:
        st.error(f"Error processing JSON data: {e}")
        return [], []

    return tree_nodes, tree_edges
def GenerateFlow():

    input_info = {
        'mood': st.session_state.get('npc_mood_text_input'),
        'personality': st.session_state.get('npc_personality_text_input'),
        'convo_additional_flavour': st.session_state.get('npc_convo_additional_flavour_text_input')
    }
    dialogue_tree_json = DTG.get_dialogue_json(input_info)
    nodes, edges = process_json(dialogue_tree_json)

    # Update the state directly
    st.session_state.curr_state.nodes = nodes
    st.session_state.curr_state.edges = edges

st.write(st.session_state)

with st.container():
    st.title("NPC Dialogue Generator")

    npc_mood_text_input = st.text_input("NPC Mood", "happy", key='npc_mood_text_input')
    npc_personality_text_input = st.text_input("NPC Personality", "friendly", key='npc_personality_text_input')
    npc_convo_additional_flavour_text_input = st.text_input("NPC Convo Additional Flavour", "pickles, groves, and the like", key='npc_convo_additional_flavour_text_input')

    generate = st.button("Generate", key='generate_button')
    if st.session_state.generate_button :
        GenerateFlow()
        st.rerun()

st.session_state.curr_state = streamlit_flow(key ='example_flow', 
                state=st.session_state.curr_state, 
                layout=TreeLayout(direction='right'), 
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

st.write(st.session_state)