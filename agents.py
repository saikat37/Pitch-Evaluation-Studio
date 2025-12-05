"""Shark Tank-style investor panel using LangGraph.

This module implements a multi-agent system with 4 shark personas:
- The Visionary (market potential, innovation)
- The Finance Shark (revenue, margins, profitability)
- The Customer Advocate (problem clarity, user value)
- The Skeptic (risks, competition, assumptions)

After all sharks provide feedback, a panel aggregator combines their
opinions into a final recommendation.
"""
import os
import json
import time
from typing import Dict, Literal
from typing_extensions import TypedDict

from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from groq import RateLimitError

load_dotenv()

# Initialize LLM with retry logic
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    max_retries=3,
)


# ================== STATE DEFINITION ==================
class PitchState(TypedDict, total=False):
    """Shared memory / state passed around the graph."""
    # Inputs from previous pipelines
    transcript: str
    tone_scores: dict
    analysis: dict

    # Persona outputs
    visionary_feedback: str
    visionary_decision: str

    finance_shark_feedback: str
    finance_shark_decision: str

    customer_advocate_feedback: str
    customer_advocate_decision: str

    skeptic_feedback: str
    skeptic_decision: str

    # Final panel output
    panel_combined_feedback: str
    panel_final_recommendation: str


# ================== PERSONA FEEDBACK MODEL & PARSER ==================
class PersonaFeedback(BaseModel):
    persona: str
    feedback: str
    decision: Literal["Invest", "Not Invest", "Need More Info"]


persona_parser = PydanticOutputParser(pydantic_object=PersonaFeedback)
persona_format_instructions = persona_parser.get_format_instructions()


# ================== GENERIC PERSONA PROMPT ==================
persona_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are {persona_name}, a virtual Shark Tank investor persona.\n"
     "Your focus: {persona_focus}.\n\n"
     "You will receive:\n"
     "- transcript: full pitch transcript (what the founder said)\n"
     "- tone_scores: JSON with vocal delivery metrics (confidence, pace, expressiveness, etc.)\n"
     "- analysis: JSON with content dimension scores and business viability.\n\n"
     "Your tasks:\n"
     "1. Read tone_scores and analysis to identify strengths and weaknesses relevant to your focus.\n"
     "2. Generate 1–2 short paragraphs of feedback in your own voice, speaking directly to the founder.\n"
     "   - Use first person (I) like on Shark Tank.\n"
     "   - Be human and conversational, not robotic.\n"
     "   - Reference specific strengths and weaknesses.\n"
     "3. End with a clear decision:\n"
     "   - Invest, Not Invest, or Need More Info.\n"
     "   - Be explicit about WHY you made that call.\n\n"
     "You MUST respond as a single JSON object with this schema:\n"
     "{format_instructions}"),
    ("user",
     "Here is the context.\n\n"
     "TRANSCRIPT:\n{transcript}\n\n"
     "TONE_SCORES (JSON):\n{tone_scores}\n\n"
     "ANALYSIS (JSON):\n{analysis}\n\n"
     "Now respond in character as {persona_name}.\n"
     "First give your feedback as natural language in the feedback field.\n"
     "Then set decision to exactly one of: Invest, Not Invest, or Need More Info."),
])


# ================== PERSONA CHAINS ==================
visionary_chain = (
    persona_prompt.partial(
        persona_name="The Visionary",
        persona_focus="market potential, long-term upside, and innovation",
        format_instructions=persona_format_instructions,
    )
    | llm
    | persona_parser
)

finance_chain = (
    persona_prompt.partial(
        persona_name="The Finance Shark",
        persona_focus="revenue model, pricing, margins, unit economics, and path to profitability",
        format_instructions=persona_format_instructions,
    )
    | llm
    | persona_parser
)

customer_chain = (
    persona_prompt.partial(
        persona_name="The Customer Advocate",
        persona_focus="problem clarity, user pain, and whether the solution truly helps customers",
        format_instructions=persona_format_instructions,
    )
    | llm
    | persona_parser
)

skeptic_chain = (
    persona_prompt.partial(
        persona_name="The Skeptic",
        persona_focus="risks, hidden assumptions, competition, and reasons this might fail",
        format_instructions=persona_format_instructions,
    )
    | llm
    | persona_parser
)


# ================== PERSONA NODE FUNCTIONS ==================
def visionary_node(state: PitchState) -> PitchState:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            res = visionary_chain.invoke({
                "transcript": state["transcript"],
                "tone_scores": json.dumps(state["tone_scores"], ensure_ascii=False),
                "analysis": json.dumps(state["analysis"], ensure_ascii=False),
            })
            return {
                "visionary_feedback": res.feedback,
                "visionary_decision": res.decision,
            }
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
            else:
                raise


def finance_node(state: PitchState) -> PitchState:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            res = finance_chain.invoke({
                "transcript": state["transcript"],
                "tone_scores": json.dumps(state["tone_scores"], ensure_ascii=False),
                "analysis": json.dumps(state["analysis"], ensure_ascii=False),
            })
            return {
                "finance_shark_feedback": res.feedback,
                "finance_shark_decision": res.decision,
            }
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise


def customer_node(state: PitchState) -> PitchState:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            res = customer_chain.invoke({
                "transcript": state["transcript"],
                "tone_scores": json.dumps(state["tone_scores"], ensure_ascii=False),
                "analysis": json.dumps(state["analysis"], ensure_ascii=False),
            })
            return {
                "customer_advocate_feedback": res.feedback,
                "customer_advocate_decision": res.decision,
            }
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise


def skeptic_node(state: PitchState) -> PitchState:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            res = skeptic_chain.invoke({
                "transcript": state["transcript"],
                "tone_scores": json.dumps(state["tone_scores"], ensure_ascii=False),
                "analysis": json.dumps(state["analysis"], ensure_ascii=False),
            })
            return {
                "skeptic_feedback": res.feedback,
                "skeptic_decision": res.decision,
            }
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise


# ================== PANEL AGGREGATOR MODEL & CHAIN ==================
class PanelOutput(BaseModel):
    combined_feedback: str
    final_recommendation: Literal["Invest", "Not Invest", "Need More Info"]


panel_parser = PydanticOutputParser(pydantic_object=PanelOutput)
panel_format_instructions = panel_parser.get_format_instructions()

panel_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are the moderator of a Shark Tank-style investor panel.\n"
     "You will receive:\n"
     "- The full pitch transcript\n"
     "- Tone scores\n"
     "- Content/viability analysis\n"
     "- Individual feedback + decisions from four sharks:\n"
     "  * The Visionary\n"
     "  * The Finance Shark\n"
     "  * The Customer Advocate\n"
     "  * The Skeptic\n\n"
     "Your job:\n"
     "1. Combine their feedback into a single, panel-style response as if you are "
     "speaking on behalf of the group.\n"
     "   - Use we language.\n"
     "   - Reference how different sharks felt (e.g., Our finance shark is worried about...).\n"
     "   - Make it sound like a real Shark Tank conversation summary.\n"
     "2. Decide a final recommendation for the panel:\n"
     "   - Invest, Not Invest, or Need More Info.\n"
     "   - Base this primarily on the sharks individual decisions.\n\n"
     "You MUST return a single JSON object with this schema:\n"
     "{format_instructions}"),
    ("user",
     "TRANSCRIPT:\n{transcript}\n\n"
     "TONE_SCORES (JSON):\n{tone_scores}\n\n"
     "ANALYSIS (JSON):\n{analysis}\n\n"
     "VISIONARY_FEEDBACK:\n{visionary_feedback}\nDecision: {visionary_decision}\n\n"
     "FINANCE_SHARK_FEEDBACK:\n{finance_shark_feedback}\nDecision: {finance_shark_decision}\n\n"
     "CUSTOMER_ADVOCATE_FEEDBACK:\n{customer_advocate_feedback}\nDecision: {customer_advocate_decision}\n\n"
     "SKEPTIC_FEEDBACK:\n{skeptic_feedback}\nDecision: {skeptic_decision}\n\n"
     "Now produce the combined panel-style feedback and the final panel recommendation."),
])

panel_chain = (
    panel_prompt.partial(format_instructions=panel_format_instructions)
    | llm
    | panel_parser
)


def panel_node(state: PitchState) -> PitchState:
    res = panel_chain.invoke({
        "transcript": state["transcript"],
        "tone_scores": json.dumps(state["tone_scores"], ensure_ascii=False),
        "analysis": json.dumps(state["analysis"], ensure_ascii=False),
        "visionary_feedback": state.get("visionary_feedback", ""),
        "visionary_decision": state.get("visionary_decision", ""),
        "finance_shark_feedback": state.get("finance_shark_feedback", ""),
        "finance_shark_decision": state.get("finance_shark_decision", ""),
        "customer_advocate_feedback": state.get("customer_advocate_feedback", ""),
        "customer_advocate_decision": state.get("customer_advocate_decision", ""),
        "skeptic_feedback": state.get("skeptic_feedback", ""),
        "skeptic_decision": state.get("skeptic_decision", ""),
    })
    return {
        "panel_combined_feedback": res.combined_feedback,
        "panel_final_recommendation": res.final_recommendation,
    }


# ================== LANGGRAPH DEFINITION ==================
def build_shark_panel_graph():
    """Build and compile the shark panel graph."""
    graph = StateGraph(PitchState)

    # Add nodes
    graph.add_node("visionary", visionary_node)
    graph.add_node("finance_shark", finance_node)
    graph.add_node("customer_advocate", customer_node)
    graph.add_node("skeptic", skeptic_node)
    graph.add_node("panel", panel_node)

    # Entry node
    def start_node(state: PitchState) -> PitchState:
        return state

    graph.add_node("start", start_node)
    graph.set_entry_point("start")

    # Edges: Sequential execution to avoid rate limits (start → visionary → finance → customer → skeptic → panel)
    graph.add_edge("start", "visionary")
    graph.add_edge("visionary", "finance_shark")
    graph.add_edge("finance_shark", "customer_advocate")
    graph.add_edge("customer_advocate", "skeptic")
    graph.add_edge("skeptic", "panel")

    # Panel → END
    graph.add_edge("panel", END)

    return graph.compile()


# Build the compiled app
shark_panel_app = build_shark_panel_graph()


def run_shark_panel(transcript: str, tone_scores: Dict, analysis: Dict) -> Dict:
    """Run the shark panel evaluation.
    
    Args:
        transcript: Full pitch transcript
        tone_scores: Tone analysis results
        analysis: Content analysis results
        
    Returns:
        Dict with individual shark feedback and panel decision
    """
    initial_state: PitchState = {
        "transcript": transcript,
        "tone_scores": tone_scores,
        "analysis": analysis,
    }
    
    result = shark_panel_app.invoke(initial_state)
    return result


__all__ = ["run_shark_panel", "shark_panel_app", "PitchState"]
