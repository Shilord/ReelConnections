import streamlit as st

from core.state import (
    init_state,
    select_mode,
    cancel_mode_selection,
    start_normal_mode,
    start_challenge_mode,
)

DIFFICULTY_OPTIONS = {
    "Easy (Top 500 actors)": "easy",
    "Medium (Top 1,500 actors)": "medium",
    "Hard (Top 5,000 actors)": "hard",
}


def render():
    init_state()

    st.markdown(
        """
        <style>
        div.stButton > button {
            font-size: 28px !important;
            font-weight: 800 !important;
            padding: 0.9rem 1rem !important;
            border-radius: 14px !important;
            white-space: nowrap !important;
            line-height: 1.1 !important;
            min-height: 72px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 style='text-align:center;'>Reel Connections</h1>",
        unsafe_allow_html=True,
        anchors=False
    )

    with st.container(border=True):
        st.markdown("<h3 style='text-align:center;'>How to Play</h3>", unsafe_allow_html=True, anchors=False)
        st.markdown(
            """
            Connect the **Start Actor** to the **Target Actor** by hopping through movies and co-stars:

            **Rules**
            1. Start from the current actor.
            2. Choose a movie that the actor appeared in.
            3. Pick a co-star from that movie to become your next current actor.
            4. Repeat until you reach the target actor.

            **Game Modes**
            - **Normal Mode**: Win in as **few steps** as possible (each movie+actor pair counts as 1 step).
            - **Challenge Mode**: Win with the **lowest total box office value** possible (each chosen movie adds its box office total to your total).

            **Difficulties**
            - **Easy**: Only the top 500 actors in terms of popularity are included.
            - **Medium**: Only the top 1,500 actors in terms of popularityare included.
            - **Hard**: All top 5,000 actors in terms of popularity are included.

            **Winning**
            - You win as soon as your current actor matches the target actor.
            - Your score is based on how your path compares to the optimal one.
            """
        )

    st.markdown("---")

    if st.session_state.pending_mode is None:
        _, col1, spacer, col2, _ = st.columns([1.2, 1.25, 0.4, 1.25, 1.2])

        with col1:
            if st.button("Normal Mode", use_container_width=True):
                select_mode("normal")
                st.rerun()

        with col2:
            if st.button("Challenge Mode", use_container_width=True):
                select_mode("challenge")
                st.rerun()

    else:
        mode_label = "Normal Mode" if st.session_state.pending_mode == "normal" else "Challenge Mode"
        st.markdown(
            f"<h3 style='text-align:center;'>{mode_label} — Choose a Difficulty</h3>",
            unsafe_allow_html=True,
            anchors=False
        )

        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            difficulty_label = st.selectbox(
                "Difficulty",
                options=list(DIFFICULTY_OPTIONS.keys()),
                key="difficulty_select",
            )

            col_confirm, col_back = st.columns(2)

            with col_confirm:
                if st.button("Confirm", use_container_width=True):
                    difficulty = DIFFICULTY_OPTIONS[difficulty_label]
                    if st.session_state.pending_mode == "normal":
                        start_normal_mode(difficulty)
                    else:
                        start_challenge_mode(difficulty)
                    st.rerun()

            with col_back:
                if st.button("Back", use_container_width=True):
                    cancel_mode_selection()
                    st.rerun()