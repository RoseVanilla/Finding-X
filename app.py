import random
import streamlit as st

st.set_page_config(page_title="Finding X", page_icon="🎯", layout="centered")

st.title("🎯 FINDING X")
st.write(
    "An **X** is hidden randomly in a 5x5 grid. Move 1 step at a time to find it within **10 moves**!"
)


# Initialize session state for game persistence across re-runs
def reset_game():
    st.session_state.prow = 0
    st.session_state.pcol = 0
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.won = False

    # Random target location (excluding starting position 0,0)
    xrow, xcol = random.randint(0, 4), random.randint(0, 4)
    while xrow == 0 and xcol == 0:
        xrow, xcol = random.randint(0, 4), random.randint(0, 4)

    st.session_state.xrow = xrow
    st.session_state.xcol = xcol
    st.session_state.msg = "Game started! Click a arrow button to move."


if "xrow" not in st.session_state:
    reset_game()


# Player movement logic
def move(direction):
    if st.session_state.game_over:
        return

    prow, pcol = st.session_state.prow, st.session_state.pcol

    if direction == "UP":
        if prow > 0:
            st.session_state.prow -= 1
        else:
            st.session_state.msg = "⚠️ Invalid move! Top border reached."
            return
    elif direction == "DOWN":
        if prow < 4:
            st.session_state.prow += 1
        else:
            st.session_state.msg = "⚠️ Invalid move! Bottom border reached."
            return
    elif direction == "LEFT":
        if pcol > 0:
            st.session_state.pcol -= 1
        else:
            st.session_state.msg = "⚠️ Invalid move! Left border reached."
            return
    elif direction == "RIGHT":
        if pcol < 4:
            st.session_state.pcol += 1
        else:
            st.session_state.msg = "⚠️ Invalid move! Right border reached."
            return

    st.session_state.moves += 1

    # Check Win / Lose conditions
    if (
        st.session_state.prow == st.session_state.xrow
        and st.session_state.pcol == st.session_state.xcol
    ):
        st.session_state.won = True
        st.session_state.game_over = True
        st.session_state.msg = (
            f"🎉 YOU WON IN {st.session_state.moves} MOVES!!"
        )
    elif st.session_state.moves >= 10:
        st.session_state.game_over = True
        st.session_state.msg = "😭 You lost! You ran out of moves."
    else:
        st.session_state.msg = f"》Not there yet! {10 - st.session_state.moves} moves remaining."


# Render 5x5 grid array
grid_display = ""
for r in range(5):
    row_cells = []
    for c in range(5):
        if st.session_state.game_over:
            if r == st.session_state.xrow and c == st.session_state.xcol:
                row_cells.append("[X]")
            elif r == st.session_state.prow and c == st.session_state.pcol:
                row_cells.append("[●]")
            else:
                row_cells.append("[  ]")
        else:
            if r == st.session_state.prow and c == st.session_state.pcol:
                row_cells.append("[●]")
            else:
                row_cells.append("[  ]")
    grid_display += "  ".join(row_cells) + "\n"

# Display game state
st.code(grid_display, language="text")

st.info(
    f"📍 Position: Row **{st.session_state.prow + 1}**, Column **{st.session_state.pcol + 1}** | Moves left: **{10 - st.session_state.moves}**"
)

st.write(f"**Status:** {st.session_state.msg}")

if st.session_state.game_over:
    st.write(
        f"🎯 **Hidden X location:** Row {st.session_state.xrow + 1}, Column {st.session_state.xcol + 1}"
    )

st.divider()

# Directional pad layout
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.button(
        "⬆️ Up (W)",
        on_click=move,
        args=("UP",),
        disabled=st.session_state.game_over,
        use_container_width=True,
    )

col_m1, col_m2, col_m3 = st.columns([1, 1, 1])
with col_m1:
    st.button(
        "⬅️ Left (A)",
        on_click=move,
        args=("LEFT",),
        disabled=st.session_state.game_over,
        use_container_width=True,
    )
with col_m2:
    st.button(
        "🔄 Play Again",
        on_click=reset_game,
        use_container_width=True,
        type="primary",
    )
with col_m3:
    st.button(
        "➡️ Right (D)",
        on_click=move,
        args=("RIGHT",),
        disabled=st.session_state.game_over,
        use_container_width=True,
    )

col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
with col_b2:
    st.button(
        "⬇️ Down (S)",
        on_click=move,
        args=("DOWN",),
        disabled=st.session_state.game_over,
        use_container_width=True,
    )
  
