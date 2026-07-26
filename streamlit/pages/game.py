import streamlit as st
from core.hints import get_realtime_hint
from core.state import init_state, submit_step, go_home, start_normal_mode
from core.game_logic import (
    calculate_shortest_path,
    calculate_lowest_boxoffice_path,
    get_movies_for_actor,
    get_actors_for_movie,
    actor_image
)


def render():
    init_state()

    data = st.session_state.game_data

    # ---------- header + hint ----------
    col_title, col_hint = st.columns([4,2])

    with col_title:
        st.markdown(
            "<h1 style='text-align:center; margin-bottom:24px;'>Normal Mode</h1>",
            unsafe_allow_html=True,
            anchors=False
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

    selected_movie_id = st.selectbox(
        "Choose a Movie",
        options=list(valid_movies.keys()),
        format_func=lambda mid: valid_movies[mid],
        key="movie_select",
    )

    # Reset the actor selection whenever the chosen movie changes, so the
    # dropdown never holds a co-star id left over from a different movie.
    if st.session_state.get("_prev_movie_select") != selected_movie_id:
        st.session_state._prev_movie_select = selected_movie_id
        st.session_state.pop("next_actor_select", None)

    cast_dict = {
        aid: name
        for aid, name in get_actors_for_movie(selected_movie_id, data).items()
        if aid != current_actor
    }

    if not cast_dict:
        st.error("No other actors found in this movie.")
        return

    next_actor_id = st.selectbox(
        "Next Actor (type to search, or open the menu to select)",
        options=list(cast_dict.keys()),
        format_func=lambda aid: cast_dict[aid],
        key="next_actor_select",
    )

    if st.button("Confirm"):
        submit_step(valid_movies[selected_movie_id], next_actor_id)
        st.rerun()

    # ---------- bottom buttons ----------
    colA, colB = st.columns(2)

    if colA.button("Restart"):
        start_normal_mode()
        st.rerun()

    if colB.button("Back to Home"):
        go_home()
        st.rerun()
