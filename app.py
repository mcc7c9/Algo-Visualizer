import streamlit as st
import random
import time

ARRAY_SIZE = 20
MIN_VALUE = 5
MAX_VALUE = 100

def generate_random_array():
    return [
        random.randint(MIN_VALUE, MAX_VALUE)
        for _ in range(ARRAY_SIZE)
    ]

def bubble_sort_steps(arr):
    a = arr[:]  # copy
    steps = []
    n = len(a)
    for i in range(n):
        swapped_in_pass = False
        for j in range(n - i - 1):
            steps.append((a[:], (j, j + 1), False))  # before compare
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped_in_pass = True
                steps.append((a[:], (j, j + 1), True))  # after swap
        if not swapped_in_pass:
            break
    steps.append((a[:], None, False))
    return steps

st.set_page_config(page_title="Algorithm Visualizer", layout="wide")

st.title("Algorithm Visualizer – Bubble Sort")

if "array" not in st.session_state:
    st.session_state.array = generate_random_array()

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("New Array"):
        st.session_state.array = generate_random_array()

    speed = st.slider("Speed (seconds per step)", 0.01, 0.5, 0.1, 0.01)

    auto_play = st.checkbox("Auto play", value=False)

array = st.session_state.array
steps = bubble_sort_steps(array)

with col2:
    placeholder = st.empty()

    def render_array(a, compare=None, swapped=False):
        # Simple bar chart using streamlit's built-in chart
        # You can also roll your own with matplotlib or altair
        import pandas as pd
        df = pd.DataFrame({"value": a})
        # Highlight logic can get fancier; start simple
        placeholder.bar_chart(df)

    if auto_play:
        for a, compare, swapped in steps:
            render_array(a, compare, swapped)
            time.sleep(speed)
    else:
        step_idx = st.slider("Step", 0, len(steps) - 1, 0)
        a, compare, swapped = steps[step_idx]
        render_array(a, compare, swapped)
