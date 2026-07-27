"""Loads and caches game data for use across the Streamlit app."""

import streamlit as st
from core.game_logic import load_data

DIFFICULTY_DATA_PATHS = {
    "easy": "data/expanded-data/game_data_easy.pkl",
    "medium": "data/expanded-data/game_data_medium.pkl",
    "hard": "data/expanded-data/game_data_hard.pkl",
}


@st.cache_data
def get_game_data(difficulty="hard"):
    """Loads game data for the given difficulty tier ("easy"/"medium"/"hard")."""
    path = DIFFICULTY_DATA_PATHS.get(difficulty, DIFFICULTY_DATA_PATHS["hard"])
    return load_data(path)
