import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout
import random
from uuid import uuid4


if 'curr_state' not in st.session_state:
    nodes = []

    edges = []

    st.session_state.curr_state = StreamlitFlowState(nodes, edges)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Add node"):
        new_node = StreamlitFlowNode(str(f"st-flow-node_{uuid4()}"), (0, 0), {'content': f'Node {len(st.session_state.curr_state.nodes) + 1}'}, 'default', 'right', 'left')
        st.session_state.curr_state.nodes.append(new_node)
        st.rerun()

with col2:
    if st.button("Delete Random Node"):
        if len(st.session_state.curr_state.nodes) > 0:
            node_to_delete = random.choice(st.session_state.curr_state.nodes)
            st.session_state.curr_state.nodes = [node for node in st.session_state.curr_state.nodes if node.id != node_to_delete.id]
            st.session_state.curr_state.edges = [edge for edge in st.session_state.curr_state.edges if edge.source != node_to_delete.id and edge.target != node_to_delete.id]
            st.rerun()

with col3:
    if st.button("Add Random Edge"):
        if len(st.session_state.curr_state.nodes) > 1:
            source = random.choice(st.session_state.curr_state.nodes)
            target = random.choice([node for node in st.session_state.curr_state.nodes if node.id != source.id])
            new_edge = StreamlitFlowEdge(f"{source.id}-{target.id}", source.id, target.id, animated=True)
            st.session_state.curr_state.edges.append(new_edge)
            st.rerun()

with col4:
    if st.button("Delete Random Edge"):
        if len(st.session_state.curr_state.edges) > 0:
            edge_to_delete = random.choice(st.session_state.curr_state.edges)
            st.session_state.curr_state.edges = [edge for edge in st.session_state.curr_state.edges if edge.id != edge_to_delete.id]
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
