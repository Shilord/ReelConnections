"""Small reusable Streamlit UI helpers shared across the game pages."""

import streamlit as st


def game_mode_title(text, help_text=None):
    """Render a centered page title with its help tooltip inline instead of pushed to the edge."""
    st.markdown("""
    <style>
    .normal-mode-title {
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: 24px;
        text-align: center !important;
    }
    /* Target the parent container when help is present */
    .element-container:has(.normal-mode-title) {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        flex-wrap: nowrap !important;
    }
    /* Keep the help icon inline */
    .element-container:has(.normal-mode-title) > div {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div class='normal-mode-title'>{text}</div>",
        unsafe_allow_html=True,
        help=help_text
    )


def format_box_office(value):
    """Format a raw box office number as an abbreviated dollar string (e.g. $1.5B)."""
    if value is None:
        return "N/A"
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.1f}T"
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    return f"${value:,}"
