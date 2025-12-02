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

def selection_sort_steps(arr):
    a = arr[:]
    steps = []
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            steps.append((a[:], (min_idx, j), False))
            if a[j] < a[min_idx]:
                min_idx = j
                steps.append((a[:], (min_idx, j), False))
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            steps.append((a[:], (i, min_idx), True))
    steps.append((a[:], None, False))
    return steps

def insertion_sort_steps(arr):
    a = arr[:]
    steps = []
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        steps.append((a[:], (j, i), False))
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
            steps.append((a[:], (j, j + 1), True))
        a[j + 1] = key
        steps.append((a[:], (j + 1, i), True))
    steps.append((a[:], None, False))
    return steps


def get_sort_steps(name, arr):
    if name == "Bubble Sort":
        return bubble_sort_steps(arr)
    if name == "Selection Sort":
        return selection_sort_steps(arr)
    if name == "Insertion Sort":
        return insertion_sort_steps(arr)
    # default fallback: return final sorted array as single step
    return [(sorted(arr), None, False)]





st.set_page_config(page_title="Algorithm Visualizer", layout="wide")

st.title("Algorithm Visualizer")

if "array" not in st.session_state:
    st.session_state.array = generate_random_array()

col1, col2 = st.columns([1, 3])

array = st.session_state.array

with col1:


    algo = st.selectbox("Algorithm", ["Bubble Sort", "Selection Sort", "Insertion Sort"])

    speed = st.slider("Speed (seconds per step)", 0.01, 0.5, 0.1, 0.01)

    if st.button("Sort"):
        # Trigger animated sorting in the right column using selected algorithm
        st.session_state.sorting = True
        st.session_state.selected_algo = algo

    if st.button("New Array"):
        st.session_state.array = generate_random_array()
        st.session_state.sorting = False





with col2:
    placeholder = st.empty()

    def render_array(a, compare=None, swapped=False):
        # Simple bar chart using streamlit's built-in chart without pandas
        placeholder.bar_chart(a)

    # Always show the current array
    render_array(array)

    # If a sort was requested, animate the steps for the selected algorithm
    if st.session_state.get("sorting", False):
        selected = st.session_state.get("selected_algo")
        steps = get_sort_steps(selected, array)
        for a, compare, swapped in steps:
            render_array(a, compare, swapped)
            time.sleep(speed)
        # ensure the session array becomes the final sorted state
        st.session_state.array = steps[-1][0]
        st.session_state.sorting = False
