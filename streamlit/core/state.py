"""Manages Streamlit session state for the Reel Connections game."""

import streamlit as st
from core.data_loader import get_game_data
from core.game_logic import generate_game

# pylint: disable=too-many-branches
def init_state():
    """Initialise all session state keys if they don't already exist."""
    # -----------------------------
    # Routing / global app state
    # -----------------------------
    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"

    # Stores the current generated game (start/target actors + optimal path, etc.)
    if "current_game" not in st.session_state:
        st.session_state.current_game = None

    # -----------------------------
    # Game state (existing fields)
    # -----------------------------
    if "mode" not in st.session_state:
        st.session_state.mode = None

    # Which mode button was clicked on the home page, awaiting a difficulty
    # selection ("normal"/"challenge"), or None while showing the mode buttons.
    if "pending_mode" not in st.session_state:
        st.session_state.pending_mode = None

    # Difficulty tier ("easy"/"medium"/"hard") the current game was started
    # with; also picks which game_data*.pkl gets loaded via get_game_data().
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = None

    if "start_actor" not in st.session_state:
        st.session_state.start_actor = None

    if "end_actor" not in st.session_state:
        st.session_state.end_actor = None

    if "current_actor" not in st.session_state:
        st.session_state.current_actor = None

    # Used in normal mode (shortest steps)
    if "step_count" not in st.session_state:
        st.session_state.step_count = 0

    # Used in challenge mode (accumulated box office)
    if "total_boxoffice" not in st.session_state:
        st.session_state.total_boxoffice = 0

    # Step history, e.g. (current_actor, movie_title_or_id, next_actor)
    if "history" not in st.session_state:
        st.session_state.history = []

    # Game end flag
    if "game_over" not in st.session_state:
        st.session_state.game_over = False

    # UI message shown on result page
    if "message" not in st.session_state:
        st.session_state.message = ""


def reset_game():
    """Reset per-game state without clearing the loaded dataset."""
    st.session_state.start_actor = None
    st.session_state.end_actor = None
    st.session_state.current_actor = None
    st.session_state.step_count = 0
    st.session_state.total_boxoffice = 0
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.current_game = None

    # Clear the movie/actor selection widgets so a leftover selection from the
    # previous game (which may not exist in the new game's options) doesn't
    # get reused and crash the selectbox on the next render.
    active_movie_key = st.session_state.pop("_active_movie_key", None)
    if active_movie_key:
        st.session_state.pop(active_movie_key, None)

    active_actor_key = st.session_state.pop("_active_actor_key", None)
    if active_actor_key:
        st.session_state.pop(active_actor_key, None)


def go_home():
    """Return to the home view and clear any active game."""
    st.session_state.current_view = "home"
    st.session_state.mode = None
    st.session_state.pending_mode = None
    reset_game()


def select_mode(mode):
    """Record which mode button was clicked, revealing the difficulty picker."""
    st.session_state.pending_mode = mode


def cancel_mode_selection():
    """Go back from the difficulty picker to the mode buttons."""
    st.session_state.pending_mode = None


def start_normal_mode(difficulty):
    """Generate a shortest-path game at the given difficulty and transition to the game view."""
    reset_game()

    st.session_state.difficulty = difficulty
    st.session_state.pending_mode = None
    st.session_state.game_data = get_game_data(difficulty)

    game = generate_game(
        "shortest",
        st.session_state.game_data
    )

    if not game["is_valid"]:
        st.session_state.message = "Could not generate a valid game. Try again."
        return

    st.session_state.mode = "normal"
    st.session_state.current_game = game
    st.session_state.start_actor = game["start_actor_id"]
    st.session_state.end_actor = game["target_actor_id"]
    st.session_state.current_actor = game["start_actor_id"]
    st.session_state.current_view = "game"


def start_challenge_mode(difficulty):
    """Generate a lowest box-office game at the given difficulty
    and transition to the challenge view."""
    reset_game()

    st.session_state.difficulty = difficulty
    st.session_state.pending_mode = None
    st.session_state.game_data = get_game_data(difficulty)

    game = generate_game(
        "box_office",
        st.session_state.game_data
    )

    if not game["is_valid"]:
        st.session_state.message = "Could not generate a valid challenge game."
        return

    st.session_state.mode = "challenge"
    st.session_state.current_game = game
    st.session_state.start_actor = game["start_actor_id"]
    st.session_state.end_actor = game["target_actor_id"]
    st.session_state.current_actor = game["start_actor_id"]
    st.session_state.current_view = "game_challenge"


def submit_step(movie_name, next_actor, movie_boxoffice=0):
    """Record a player step, advance the current actor, and check the win condition."""
    st.session_state.history.append((st.session_state.current_actor, movie_name, next_actor))
    st.session_state.current_actor = next_actor

    # Update score counters depending on mode
    if st.session_state.mode == "normal":
        st.session_state.step_count += 1
    elif st.session_state.mode == "challenge":
        st.session_state.total_boxoffice += int(movie_boxoffice or 0)

    # Check win condition
    if st.session_state.current_actor == st.session_state.end_actor:
        st.session_state.game_over = True
        st.session_state.current_view = "result"
        st.session_state.message = "🎉 You connected to the target actor!"


def end_game_with_fail(reason=""):
    """Force-end the game and display a message on the result page."""
    st.session_state.game_over = True
    st.session_state.current_view = "result"
    st.session_state.message = reason or "Game ended"
