from crewai import Task

def analyze_profile(agent, user_input, memory_context=""):
    return Task(
        description=f"""
        Previous user memory (if any):
        {memory_context}

        Analyze the following user profile:
        {user_input}

        Extract:
        - Education
        - Skills
        - Interests
        """,
        agent=agent,
        expected_output="Structured profile analysis"
    )

def skill_gap(agent, profile_task):
    return Task(
        description="""
        Use ONLY the Profile Analyzer output from context.
        Identify the top 5 skill gaps for AI/Data Science careers.
        For each gap, provide:
        - Current level (Beginner/Intermediate/Advanced)
        - Why it matters
        - Priority (High/Medium/Low)
        """,
        agent=agent,
        context=[profile_task],
        expected_output="Top 5 prioritized skill gaps with reasons and current level"
    )

def recommend_courses(agent, skill_gap_task):
    return Task(
        description="""
        Use ONLY the Skill Gap Analyzer output from context.
        Recommend realistic, currently available courses that map directly
        to each high/medium-priority skill gap.
        For each course include:
        - Skill gap addressed
        - Course title
        - Platform
        - Difficulty (Beginner/Intermediate/Advanced)
        - Estimated duration
        """,
        agent=agent,
        context=[skill_gap_task],
        expected_output="Gap-mapped course list with platform, level, and duration"
    )

def career_advice(agent, profile_task, skill_gap_task, course_task):
    return Task(
        description="""
                Use ALL prior task outputs from context.

                Write a well-structured and engaging final counseling response.

                Requirements:
                - Use a friendly, professional career counselor tone.
                - Personalize the advice to the user's profile and skills
                    (for example React, Python, C++, ML basics where relevant).
                - Avoid generic statements.
                - Explain recommendations briefly instead of only listing them.
                - Keep the structure clean, readable, and non-repetitive.

                Include these sections with bold headings:

                1. Career Direction
                Explain suitable career options and why each one fits the user.

                2. Key Skills to Focus
                Explain which skills matter most and why they are important.

                3. Learning Plan
                Provide a clear 6-8 week plan with meaningful, practical steps.

                4. Recommended Courses
                Suggest realistic, currently available courses from prior context,
                and add a short reason for each recommendation.

                5. Practical Next Steps
                Give actionable next steps and include at least one concrete
                project idea combining the user's skills.

                Formatting guidance:
                - Start with a 1-2 line insight summary about the user's potential.
                - Use short paragraphs with spacing between sections.
                - Avoid long bullet dumps.
        """,
        agent=agent,
        context=[profile_task, skill_gap_task, course_task],
                expected_output="Personalized, insight-driven 5-section roadmap with short explanations and one concrete project idea"
    )