from flask import Flask, render_template, request, jsonify
from crewai import Crew, Agent, Task
import requests
import os

# --- Conceptual Diagram Generation (Replace with actual AI integration) ---
def generate_diagram(problem_description: str):
    """
    Conceptually generates a diagram filename based on the problem description.
    In a real application, this would involve calling an AI model to create an image.
    For this example, we'll just return a placeholder filename.
    """
    filename = f"diagrams/{problem_description.replace(' ', '_')}.png"
    # In a real scenario, you would save the generated image to this path
    return filename

# --- Conceptual Diagram Storage (Replace with actual storage) ---
DIAGRAM_FOLDER = 'static/diagrams'
os.makedirs(DIAGRAM_FOLDER, exist_ok=True)

# --- Conceptual Diagram Search (Replace with actual search) ---
def search_diagrams(search_term: str):
    """
    Conceptually searches for diagram filenames containing the search term.
    In a real application, this might involve querying a database or using more sophisticated search.
    """
    diagram_files = [f for f in os.listdir(DIAGRAM_FOLDER) if f.endswith(".png")]
    results = [f"/static/diagrams/{f}" for f in diagram_files if search_term.lower() in f.lower()]
    return results

app = Flask(__name__)

# Define a simple CrewAI Agent and Task setup
agent = Agent(
    role="Problem Solver",
    goal="Find solutions to social problems and visualize them.",
    backstory="An experienced policy maker and humanitarian expert with a knack for visual communication.",
    allow_delegation=False,
    verbose=True
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    diagram_url = None
    if request.method == "POST":
        user_input = request.form.get("prompt")

        # Define the Task based on user input
        task = Task(
            description=f"Analyze and propose solutions for this social issue: {user_input}. Also, think about a simple visual representation (a diagram concept) for this problem.",
            expected_output="Detailed, actionable steps to address the problem, and a description of a relevant diagram concept.",
            agent=agent
        )

        # Create a Crew instance with the agent and task
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )

        try:
            # Execute the tasks and get the result
            analysis_result = crew.kickoff()
            result = analysis_result

            # --- Conceptual Diagram Generation ---
            diagram_filename = generate_diagram(user_input)
            # In a real application, you would now have an AI-generated image at this path
            diagram_url = diagram_filename

        except Exception as e:
            result = f"An error occurred: {str(e)}"

    return render_template("index.html", result=result, diagram_url=diagram_url)

@app.route("/search_diagrams", methods=["POST"])
def search_diagrams_route():
    search_term = request.form.get("search_term")
    if search_term:
        diagram_results = search_diagrams(search_term)
        return jsonify(diagrams=diagram_results)
    return jsonify(diagrams=[])

if __name__ == "__main__":
    app.run(debug=True)