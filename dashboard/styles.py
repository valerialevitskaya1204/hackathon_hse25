import streamlit as st

def init_styles():
    st.markdown(
        """
        <style>
        [data-testid="block-container"] {
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 1rem;
            padding-bottom: 0rem;
            margin-bottom: -7rem;
        }

        [data-testid="stVerticalBlock"] {
            padding-left: 0rem;
            padding-right: 0rem;
        }
        [data-testid="stMetric"] {
            text-align: left;
            padding: 15px 0;
            margin-left: 4px;
        }

        [data-testid="stMetricLabel"] {
        display: none;
        justify-content: center;
        align-items: center;
        }

        [data-testid="stMetricValue"] {
        justify-content: center;
        align-items: center;
        font-size: 4rem;
        }

        [data-testid="stMetricDelta"] {
        justify-content: left;
        align-items: left;
        font-size: 1.5rem;
        }
        [data-testid="stMetricDeltaIcon-Up"] {
            position: relative;
            left: 38%;
            -webkit-transform: translateX(-50%);
            -ms-transform: translateX(-50%);
            transform: translateX(-50%);
        }

        [data-testid="stMetricDeltaIcon-Down"] {
            position: relative;
            left: 38%;
            -webkit-transform: translateX(-50%);
            -ms-transform: translateX(-50%);
            transform: translateX(-50%);
        }
        </style>
        """,
        unsafe_allow_html=True
)