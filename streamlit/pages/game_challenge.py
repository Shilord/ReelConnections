import streamlit as st
from core.hints import get_realtime_hint
from core.state import (
    init_state,
    submit_step,
    go_home,
    start_challenge_mode,
)

from core.game_logic import (
    calculate_shortest_path,
    calculate_lowest_boxoffice_path,
    get_movies_for_actor,
    get_actors_for_movie,
    actor_image
)

def format_box_office(value):
    if value is None:
        return "N/A"
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.1f}T"
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    return f"${value:,}"

def render():
    init_state()

    data = st.session_state.game_data

    # ---------- header + hint ----------
    col_title, col_hint = st.columns([4,2])

    with col_title:
        st.markdown(
            "<h1 style='text-align:center; margin-bottom:10px;'>Challenge Mode</h1>",
            unsafe_allow_html=True,
            anchors=False
        )

        st.markdown(
            f"<p style='text-align:center; font-size:18px;'>"
            f"Total Box Office: {format_box_office(st.session_state.total_boxoffice)}</p>",
            unsafe_allow_html=True,
        )

    with col_hint:
        with st.expander("💡 Hint", expanded=False):

            current_actor = st.session_state.current_actor
            target_actor = st.session_state.end_actor
            mode = st.session_state.mode

            if mode == "normal":
                hint_result = calculate_shortest_path(current_actor, target_actor, data)
            elif mode == "challenge":
                hint_result = calculate_lowest_boxoffice_path(current_actor, target_actor, data)
            else:
                hint_result = None

            if hint_result and hint_result["is_successful"] and hint_result["path"]:
                movie_id, actor_id = hint_result["path"][0]

                movie_title = data["movies"][movie_id]["title"]
                actor_name = data["actors"][actor_id]["name"]

                st.write("Best next move:")
                st.write(f"🎬 Movie: **{movie_title}**")
                st.write(f"🎭 Actor: **{actor_name}**")
            else:
                st.write("No hint available.")

    # ---------- actors ----------
    current_actor = st.session_state.current_actor
    target_actor = st.session_state.end_actor

    current_name = data["actors"][current_actor]["name"]
    target_name = data["actors"][target_actor]["name"]

    # ---------- actor cards ----------
    col_left, col_right = st.columns(2)

    with col_left:
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            st.markdown(
                "<h4 style='text-align:center;'>Current Actor</h4>",
                unsafe_allow_html=True,
                anchors=False
            )

            image = actor_image(current_actor)
            if image:
                st.image(image, caption=current_name, width=185)
            else:
                st.info(f"No photo available for {current_name}.")

    with col_right:
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            st.markdown(
                "<h4 style='text-align:center;'>Target Actor</h4>",
                unsafe_allow_html=True,
                anchors=False
            )

            image = actor_image(target_actor)
            if image:
                st.image(image, caption=target_name, width=185)
            else:
                st.info(f"No photo available for {target_name}.")

    st.markdown("---")

    # ---------- movie + actor selection ----------
    valid_movies = get_movies_for_actor(current_actor, data)

    if not valid_movies:
        st.error("No movies found for this actor.")
        return

    st.markdown(
        """
        <style>
        div.st-key-selection_box {
            background-color: rgba(125, 125, 125, 0.06);
            border: 1px solid rgba(125, 125, 125, 0.2);
            border-radius: 14px;
            padding: 1.5rem 1.75rem 1.75rem;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            margin-bottom: 3rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="selection_box"):
        # Keying the widget by the current actor forces it to remount whenever
        # the actor changes (including on Restart), so the movie selection is
        # forcibly reset instead of silently keeping the previous actor's
        # selection until the user manually interacts with the dropdown.
        movie_key = f"movie_select_{current_actor}"
        prev_movie_key = st.session_state.get("_active_movie_key")
        if prev_movie_key and prev_movie_key != movie_key:
            st.session_state.pop(prev_movie_key, None)
        st.session_state._active_movie_key = movie_key

        selected_movie_id = st.selectbox(
            "Choose a Movie",
            options=list(valid_movies.keys()),
            format_func=lambda mid: valid_movies[mid],
            key=movie_key,
        )

        cast_dict = {
            aid: name
            for aid, name in get_actors_for_movie(selected_movie_id, data).items()
            if aid != current_actor
        }

        if not cast_dict:
            st.error("No other actors found in this movie.")
            return

        # Keying the widget by the selected movie forces it to remount whenever
        # the movie changes, so the actor selection is forcibly reset to that
        # movie's cast instead of silently keeping the previous movie's
        # selection until the user manually interacts with the dropdown.
        actor_key = f"next_actor_select_{selected_movie_id}"
        prev_actor_key = st.session_state.get("_active_actor_key")
        if prev_actor_key and prev_actor_key != actor_key:
            st.session_state.pop(prev_actor_key, None)
        st.session_state._active_actor_key = actor_key

        next_actor_id = st.selectbox(
            "Next Actor (type to search, or open the menu to select)",
            options=list(cast_dict.keys()),
            format_func=lambda aid: cast_dict[aid],
            key=actor_key,
        )

        if st.button("Confirm"):
            boxoffice = data["movies"][selected_movie_id]["box_office"]
            submit_step(
                valid_movies[selected_movie_id],
                next_actor_id,
                movie_boxoffice=boxoffice,
            )
            st.rerun()

    # ---------- bottom buttons ----------
    colA, colB = st.columns(2)

    if colA.button("Restart"):
        start_challenge_mode(st.session_state.difficulty)
        st.rerun()

    if colB.button("Back to Home"):
        go_home()
        st.rerun()
