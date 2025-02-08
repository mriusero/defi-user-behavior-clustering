import streamlit as st

def load_html(file_path):
    """Charge le fichier HTML et le met en cache."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def display_graph(selection):
    """Affiche le graphique sélectionné."""
    graph_paths = {
        "Address-Protocol Graph": "docs/graphics/network/address_protocol_graph.html",
        "Address-Protocol-Type Graph": "docs/graphics/network/address_protocol_type_graph.html",
        "Address-Address Graph": "docs/graphics/network/address_address_graph.html",
    }
    if selection == "Address-Protocol-Type Graph":
        note = """
        # Address-Protocol-Type Graph
        This graph shows the connections between addresses and protocol-type (Stable-coins, Lending, NFT...). \n
        > It contains only 10000 transactions against the full dataset of + 6,8 M transactions.
        """
    elif selection == "Address-Protocol Graph":
        note = """
        # Address-Protocol Graph
        This graph shows the connections between addresses and protocols (Uniswap, Tether, USDC, NFT-Fi...).\n
        > It contains only 10000 transactions against the full dataset of + 6,8 M transactions.
        """
    else:
        note = """
        # Address-Address Graph
        This graph shows the connections between addresses based on transactions.\n
        > It contains only 10000 transactions against the full dataset of + 22M transactions.
        """

    st.write(note)
    st.components.v1.html(load_html(graph_paths[selection]), height=800)


def page_1():
    st.markdown(
        '<div class="header">Detected User Profiles_</div>',
        unsafe_allow_html=True,
    )

    with st.form(key="graph_form"):
        selection = st.selectbox(
            "Select graph to visualize",
            ["Address-Address Graph", "Address-Protocol Graph", "Address-Protocol-Type Graph"],
        )
        submit_button = st.form_submit_button("Display Graph")

    if submit_button:
        display_graph(selection)