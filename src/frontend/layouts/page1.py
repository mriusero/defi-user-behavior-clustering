import streamlit as st

def page_1():
    st.markdown(
        '<div class="header">Detected User Profiles_</div>',
        unsafe_allow_html=True,
    )
    st.write("> These graphs only contains 1 000 000 users against 6 870 000 in the real dataset.")

    col1, col2 = st.columns(2)
    with col1:
        st.write("### Protocols Network")
        st.image("docs/graphics/address_protocol/address_protocol_nx_plot.png", caption="")

        st.write("### Transactions Numbers *(standardised)*")
        st.image("docs/graphics/exploratory_analysis/transactions_numbers.png", caption="")
    with col2:
        st.write("### Protocol Types Network")
        st.image("docs/graphics/address_protocol/address_protocol_type_nx_plot.png", caption="")

        st.write("### Transactions Values *(standardised)*")
        st.image("docs/graphics/exploratory_analysis/transactions_values.png", caption="")

    st.write("### Pairplot (PCA reduced features)")
    st.image("docs/graphics/exploratory_analysis/pairplot_pca.png", caption="")