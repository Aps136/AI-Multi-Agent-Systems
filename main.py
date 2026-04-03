from crewai import Crew
from agents import (
    profile_analyzer,
    skill_gap_analyzer,
    course_recommender,
    career_advisor
)
from tasks import (
    analyze_profile,
    skill_gap,
    recommend_courses,
    career_advice
)
import json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

MEMORY_FILE = Path("career_memory.json")


def load_recent_memory(limit=3):
    if not MEMORY_FILE.exists():
        return "No previous user history available."

    try:
        data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not data:
            return "No previous user history available."

        recent = data[-limit:]
        lines = []
        for item in recent:
            profile = item.get("user_input", "")
            summary = item.get("summary", "")
            lines.append(f"- Profile: {profile}\n  Previous Summary: {summary}")
        return "\n".join(lines)
    except Exception:
        return "No previous user history available."


def save_memory(user_input, output_text):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_input": user_input,
        "summary": str(output_text).replace("\n", " ")[:280],
    }

    data = []
    if MEMORY_FILE.exists():
        try:
            loaded = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
            if isinstance(loaded, list):
                data = loaded
        except Exception:
            data = []

    data.append(entry)
    MEMORY_FILE.write_text(json.dumps(data[-30:], indent=2), encoding="utf-8")

def run_career_counselor(user_input):
    memory_context = load_recent_memory()

    # Create agents
    agent1 = profile_analyzer()
    agent2 = skill_gap_analyzer()
    agent3 = course_recommender()
    agent4 = career_advisor()

    # Create tasks
    task1 = analyze_profile(agent1, user_input, memory_context)
    task2 = skill_gap(agent2, task1)
    task3 = recommend_courses(agent3, task2)
    task4 = career_advice(agent4, task1, task2, task3)

    # Create crew
    crew = Crew(
        agents=[agent1, agent2, agent3, agent4],
        tasks=[task1, task2, task3, task4],
        verbose=False
    )

    try:
        result = crew.kickoff()
        save_memory(user_input, result)
        return result
    except Exception as e:
        error_text = str(e)
        if "model_decommissioned" in error_text or "decommissioned" in error_text:
            return (
                "Selected model is deprecated on provider side. Update the model name "
                "in agents.py and run again."
            )
        if "invalid_api_key" in error_text or "Invalid API Key" in error_text:
            return (
                "Invalid LLM API key. If using Groq, set a valid GROQ_API_KEY in .env "
                "and try again."
            )
        if "insufficient_quota" in error_text or "Error code: 429" in error_text:
            return (
                "LLM API quota exceeded. Please check billing/quota for your provider API key "
                "and try again."
            )
        raise


if __name__ == "__main__":
    user_input = input("Enter your profile: ")
    output = run_career_counselor(user_input)
    print("\nFINAL OUTPUT:\n")
    print(output)