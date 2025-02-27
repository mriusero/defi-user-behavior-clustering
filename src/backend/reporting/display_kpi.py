import streamlit as st


def display_kpi(user_data, global_radar, cluster_radar):
    """ Display user rates on progress bars with custom CSS. """

    # Display the radar charts with progress bars
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

    st.markdown(custom_css, unsafe_allow_html=True)

    st.write("#### Cluster Performance_")
    st.write("---")
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.pyplot(cluster_radar)

    with col2:
        for name, (description, global_rank, cluster_rank) in list(metrics.items())[:10]:
            progress_width = f"{cluster_rank * 100}%"
            percentage = f"{cluster_rank * 100:.1f}%"
            st.markdown(f"""
                            <div class='progress-container'>
                                <div class='progress-bar' style='width: {progress_width};'></div>
                                <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage})</div>
                            </div>
                            """, unsafe_allow_html=True)

    with col3:
        for name, (description, global_rank, cluster_rank) in list(metrics.items())[10:]:
            progress_width = f"{cluster_rank * 100}%"
            percentage = f"{cluster_rank * 100:.1f}%"
            st.markdown(f"""
                            <div class='progress-container'>
                                <div class='progress-bar' style='width: {progress_width};'></div>
                                <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage}</div>
                            </div>
                            """, unsafe_allow_html=True)


    st.write("#### Global Performance_")
    st.write("---")
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.pyplot(global_radar)

    with col2:
        for name, (description, global_rank, cluster_rank) in list(metrics.items())[:10]:
            progress_width = f"{global_rank * 100}%"
            percentage = f"{global_rank * 100:.1f}%"
            st.markdown(f"""
                        <div class='progress-container'>
                            <div class='progress-bar' style='width: {progress_width};'></div>
                            <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage})</div>
                        </div>
                        """, unsafe_allow_html=True)

    with col3:
        for name, (description, global_rank, cluster_rank) in list(metrics.items())[10:]:
            progress_width = f"{global_rank * 100}%"
            percentage = f"{global_rank * 100:.1f}%"
            st.markdown(f"""
                        <div class='progress-container'>
                            <div class='progress-bar' style='width: {progress_width};'></div>
                            <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage})</div>
                        </div>
                        """, unsafe_allow_html=True)