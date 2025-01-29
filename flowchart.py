import os
from graphviz import Digraph

# Create a flowchart
flowchart = Digraph(format="png", graph_attr={"rankdir": "TB"}, node_attr={"shape": "rectangle", "style": "rounded"})

# Add nodes with specified shapes and content
flowchart.node("Input", "User Input (Text or Speech)", shape="rect", style="rounded")
flowchart.node("Preprocessing", """Preprocessing :\n• Tokenization\n• Stemming\n• Lemmatization\n• POS Tagging""")
flowchart.node("TenseDetection", "Tense Detection")
flowchart.node("StopWordRemoval", "Stop Word Removal")
flowchart.node("AnimationLookup", "Animation Lookup (Word by Word)")
flowchart.node("AnimationPlayback", "Animation Playback\n", shape="rect", style="rounded")

# Add edges to connect the steps
flowchart.edges([
    ("Input", "Preprocessing"),
    ("Preprocessing", "TenseDetection"),
    ("TenseDetection", "StopWordRemoval"),
    ("StopWordRemoval", "AnimationLookup"),
    ("AnimationLookup", "AnimationPlayback"),
])

# Define the file path
file_path = "c:/Users/dawnj/OneDrive/Documents/project/Audio-Speech-To-Sign-Language-Converter-master/flowchart_speech_to_animation"

# Create the directory if it does not exist
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Save and render the flowchart
flowchart.render(file_path, format="png", cleanup=True)

file_path + ".png"
