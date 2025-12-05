"""Pydantic output parsers and model schemas used by the pipeline.
These mirror the structures expected by the LLM chains.
"""
from pydantic import BaseModel, conint
from typing import List


class ScoreReason(BaseModel):
    score: conint(ge=0, le=100)
    reason: str


class PitchStructureResult(BaseModel):
    hook_present: bool
    problem_present: bool
    solution_present: bool
    ask_present: bool
    detected_order: List[str]
    structure_quality_score: conint(ge=0, le=100)
    structure_comment: str


class BusinessViabilityResult(BaseModel):
    score: conint(ge=0, le=100)
    risk_level: str
    summary_comment: str
    key_strengths: List[str]
    key_risks: List[str]


class PersonaFeedback(BaseModel):
    feedback: str
    decision: str


class PanelOutput(BaseModel):
    panel_feedback: str
    panel_decision: str


__all__ = [
    "ScoreReason",
    "PitchStructureResult",
    "BusinessViabilityResult",
    "PersonaFeedback",
    "PanelOutput",
]
