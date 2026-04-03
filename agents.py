from crewai import Agent

# CrewAI Agent.llm expects a provider/model string or CrewAI BaseLLM.
llm = "groq/llama-3.3-70b-versatile"

def profile_analyzer():
    return Agent(
        role="Profile Analyzer",
        goal="Understand the user's background, education, and interests",
        backstory="Expert in analyzing student and professional profiles.",
        llm=llm,
        verbose=False
    )

def skill_gap_analyzer():
    return Agent(
        role="Skill Gap Analyzer",
        goal="Identify missing skills required for target careers",
        backstory="Specialist in identifying skill gaps in tech careers.",
        llm=llm,
        verbose=False
    )

def course_recommender():
    return Agent(
        role="Course Recommender",
        goal="Recommend relevant courses to fill skill gaps",
        backstory="Recommends ONLY realistic and currently available courses from Coursera, Udemy, etc.",
        llm=llm,
        verbose=False
    )

def career_advisor():
    return Agent(
        role="Career Advisor",
        goal="Suggest suitable career paths with roadmap",
        backstory="Experienced career counselor helping students choose paths.",
        llm=llm,
        verbose=False
    )