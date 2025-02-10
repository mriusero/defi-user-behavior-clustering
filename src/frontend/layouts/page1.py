import streamlit as st

def page_1():
    st.markdown(
        '<div class="header">Detected User Profiles_</div>',
        unsafe_allow_html=True,
    )
    st.write("> These graphs only contains 1 000 000 users against 6 870 000 in the real dataset.")

    st.write("### Address Protocol Network")
    st.image("docs/graphics/address_protocol/address_protocol_nx_plot_0.png", caption="")

    st.write("### Address Protocol Network")
    st.image("docs/graphics/address_protocol/address_protocol_nx_plot_1.png", caption="")