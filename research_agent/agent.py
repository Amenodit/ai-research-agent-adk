from google.adk.agents.llm_agent import Agent
from duckduckgo_search import DDGS
import math

# 🔧 TOOL 1: Research Topic (basic explanation)
def research_topic(topic: str) -> str:
    print(f"[TOOL USED] research_topic: {topic}")
    return f"Here is a detailed explanation about: {topic}"

# 🔧 TOOL 2: Safe Calculator
def calculate(expression: str) -> str:
    print(f"[TOOL USED] calculate: {expression}")
    try:
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except:
        return "Invalid calculation"

# 🔧 TOOL 3: Real Web Search
def web_search(query: str) -> str:
    print(f"[TOOL USED] web_search: {query}")
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(
                    f"Title: {r['title']}\n"
                    f"Summary: {r['body']}\n"
                    f"Link: {r['link']}\n"
                )
        return "\n".join(results)
    except:
        return "Error fetching search results"

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 🔧 TOOL 4: Create PDF
def create_pdf(content: str) -> str:
    print(f"[TOOL USED] create_pdf")

    try:
        file_name = "research_output.pdf"

        doc = SimpleDocTemplate(file_name)
        styles = getSampleStyleSheet()

        story = []

        # Split content into paragraphs
        for line in content.split("\n"):
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 10))

        doc.build(story)

        return f"PDF created successfully: {file_name}"

    except Exception as e:
        return f"Error creating PDF: {str(e)}"

# 🧠 MAIN AGENT
root_agent = Agent(
    model='gemini-2.5-flash',
    name='research_agent',
    description='Advanced AI Research Assistant with tools',
    instruction="""
You are an advanced AI research assistant.

RULES:
- Use web_search for latest or real-world information
- Use research_topic for general explanations
- Use calculate for math problems
- Always combine tool output with your own explanation
- Give structured answers (headings, bullet points)
- Be clear, informative, and concise
- Use create_pdf when user asks to save or export content as PDF
""",
    tools=[research_topic, calculate, web_search, create_pdf]
)