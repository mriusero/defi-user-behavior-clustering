import streamlit as st
from pyarrow import feather

from src.backend.core.ranking import fetch_rank
from src.backend.core.plot_radar import plot_radar_chart

@st.cache_data
def pre_load_ranks():
    ranks = feather.read_table('src/frontend/layouts/data/users_scored.arrow').to_pandas()
    return ranks



def page_4():
    st.markdown('<div class="header">Who am I ?</div>', unsafe_allow_html=True)

    st.markdown("""
    Give me your ethereum address and I will tell who you are.
    """)
    ranks = pre_load_ranks()
    st.write(ranks.sample(5))
    address = st.text_input("Address", value="0xbc8cbb3bcad18cd64de04a6d53503ccced07ef5b")

    if st.button("Submit"):
        st.write(f"If your address is `{address}` then your performances are :")

        user_data = fetch_rank(ranks, address)

        col1, col2 = st.columns([1, 1])
        global_radar = plot_radar_chart(ranks, user_data, to_plot='global_rank')
        cluster_radar = plot_radar_chart(ranks, user_data, to_plot='cluster_rank')
        with col1:
            st.pyplot(global_radar)
        with col2:
            st.pyplot(cluster_radar)

        st.write("---")
        st.json(user_data)
        st.write("---")

        metrics = {}
        for metric in user_data['performances']:
            name = metric['name']
            description = metric['description']
            cluster_rank = metric['cluster_rank']
            global_rank = metric['global_rank']
            metrics[name] = (description, global_rank, cluster_rank)

        custom_css = """
        <style>
        .progress-container {
            position: relative;
            width: 100%;
            height: 40px;
            background-color: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        .progress-bar {
            height: 100%;
            background-color: #1e8b22;
            position: absolute;
            top: 0;
            left: 0;
            border-radius: 5px;
        }
        .progress-text {
            position: absolute;
            width: 100%;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            line-height: 40px;
            color: #333;
        }
        </style>
        """

        # Afficher le CSS personnalisé
        st.markdown(custom_css, unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 2])

        with col1:
            st.write("#### Global Performance")
            st.write("---")
            for name, (description, global_rank, cluster_rank) in list(metrics.items())[:10]:
                progress_width = f"{global_rank * 100}%"
                percentage = f"{global_rank * 100:.1f}%"
                st.markdown(f"""
                <div class='progress-container'>
                    <div class='progress-bar' style='width: {progress_width};'></div>
                    <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage})</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.write("#### ")
            st.write("---")
            for name, (description, global_rank, cluster_rank) in list(metrics.items())[10:]:
                progress_width = f"{global_rank * 100}%"
                percentage = f"{global_rank * 100:.1f}%"
                st.markdown(f"""
                <div class='progress-container'>
                    <div class='progress-bar' style='width: {progress_width};'></div>
                    <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage})</div>
                </div>
                """, unsafe_allow_html=True)

        with col4:
            st.write("#### Cluster Performance")
            st.write("---")
            for name, (description, global_rank, cluster_rank) in list(metrics.items())[:10]:
                progress_width = f"{cluster_rank * 100}%"
                percentage = f"{cluster_rank * 100:.1f}%"
                st.markdown(f"""
                <div class='progress-container'>
                    <div class='progress-bar' style='width: {progress_width};'></div>
                    <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage})</div>
                </div>
                """, unsafe_allow_html=True)

        with col5:
            st.write("#### ")
            st.write("---")
            for name, (description, global_rank, cluster_rank) in list(metrics.items())[10:]:
                progress_width = f"{cluster_rank * 100}%"
                percentage = f"{cluster_rank * 100:.1f}%"
                st.markdown(f"""
                <div class='progress-container'>
                    <div class='progress-bar' style='width: {progress_width};'></div>
                    <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage}</div>
                </div>
                """, unsafe_allow_html=True)
