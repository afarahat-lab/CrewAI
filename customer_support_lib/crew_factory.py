from crewai import Agent, Crew, CrewOutput, Task
from crewai.types.streaming import CrewStreamingOutput
from crewai.llm import LLM


def create_crew(llm: LLM, verbose: bool = False) -> Crew:
    support_agent = Agent(
        role="Senior Support Representative",
        goal="Be the most friendly and helpful "
            "support representative in your team",
        backstory=(
            "You work at crewAI (https://crewai.com) and "
            " are now working on providing "
            "support to {customer}, a super important customer "
            " for your company."
            "You need to make sure that you provide the best support!"
            "Make sure to provide full complete answers, "
            " and make no assumptions."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    support_quality_assurance_agent = Agent(
        role="Support Quality Assurance Specialist",
        goal="Get recognition for providing the "
        "best support quality assurance in your team",
        backstory=(
            "You work at crewAI (https://crewai.com) and "
            "are now working with your team "
            "on a request from {customer} ensuring that "
            "the support representative is "
            "providing the best support possible.\n"
            "You need to make sure that the support representative "
            "is providing full"
            "complete answers, and make no assumptions.\n"
            "When delegating work, call the delegation tool with real values only. "
            "The input must be an object with exactly these top-level keys: "
            "task, context, coworker. "
            "Never pass schema metadata like properties, required, title, or type.\n"
            "Use coworker exactly as: Senior Support Representative."
        ),
        verbose=True,
        llm=llm,
        allow_delegation=True
    )

    from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool
    
    docs_scrape_tool = ScrapeWebsiteTool(
        website_url="https://docs.crewai.com/en/tools/overview"
    )

    inquiry_resolution = Task(
        description=(
            "{customer} just reached out with a super important ask:\n"
            "{inquiry}\n\n"
            "{person} from {customer} is the one that reached out. "
            "Make sure to use everything you know "
            "to provide the best support possible."
            "You must strive to provide a complete "
            "and accurate response to the customer's inquiry."
        ),
        expected_output=(
            "A detailed, informative response to the "
            "customer's inquiry that addresses "
            "all aspects of their question.\n"
            "The response should include references "
            "to everything you used to find the answer, "
            "including external data or solutions. "
            "Ensure the answer is complete, "
            "leaving no questions unanswered, and maintain a helpful and friendly "
            "tone throughout."
        ),
        tools=[docs_scrape_tool],
        agent=support_agent,
    )

    quality_assurance_review = Task(
        description=(
            "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
            "Ensure that the answer is comprehensive, accurate, and adheres to the "
            "high-quality standards expected for customer support.\n"
            "Verify that all parts of the customer's inquiry "
            "have been addressed "
            "thoroughly, with a helpful and friendly tone.\n"
            "Check for references and sources used to "
            " find the information, "
            "ensuring the response is well-supported and "
            "leaves no questions unanswered.\n"
            "If you delegate, the tool input must be valid JSON with top-level fields "
            "task, context, coworker (string values). "
            "Do not send tool schema definitions."
        ),
        expected_output=(
            "A final, detailed, and informative response "
            "ready to be sent to the customer.\n"
            "This response should fully address the "
            "customer's inquiry, incorporating all "
            "relevant feedback and improvements.\n"
            "Don't be too formal, we are a chill and cool company "
            "but maintain a professional and friendly tone throughout."
            "Output should be in the form of email with steps to resolve the issue, and any references used."
        ),
        agent=support_quality_assurance_agent,
    )


    return Crew(
        agents=[support_agent, support_quality_assurance_agent],
        tasks=[inquiry_resolution, quality_assurance_review],
        verbose=False,
        memory=True
    )

def run_crew(llm: LLM, verbose: bool = False) -> CrewOutput | CrewStreamingOutput:
    crew = create_crew(llm=llm, verbose=verbose)
    return crew.kickoff(inputs = {
        "customer": "DeepLearningAI",
        "person": "Andrew Ng",
        "inquiry": "How can I create a crew that read information from documents, a website and provide feedback for users"
    })