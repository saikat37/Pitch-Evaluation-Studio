"""Main backend logic for LLM-based content analysis using langchain_groq.

This module exposes `analyze_pitch_with_viability` which uses real LLM chains
to evaluate pitch dimensions, structure, and business viability.
"""
import os
import json
from typing import Dict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableParallel

from parsers import (
    ScoreReason,
    PitchStructureResult,
    BusinessViabilityResult,
)
from prompts import (
    build_problem_prompt,
    build_product_diff_prompt,
    build_business_model_prompt,
    build_market_prompt,
    build_revenue_prompt,
    build_competition_prompt,
    build_structure_prompt,
    build_viability_prompt,
)

load_dotenv()

# Initialize LLM with retry logic for rate limits
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY"),
    max_retries=3,
)

# Initialize parsers
score_reason_parser = PydanticOutputParser(pydantic_object=ScoreReason)
structure_parser = PydanticOutputParser(pydantic_object=PitchStructureResult)
viability_parser = PydanticOutputParser(pydantic_object=BusinessViabilityResult)

# Format instructions with escaped braces
_score_instructions = score_reason_parser.get_format_instructions().replace('{', '{{').replace('}', '}}')
_structure_instructions = structure_parser.get_format_instructions().replace('{', '{{').replace('}', '}}')
_viability_instructions = viability_parser.get_format_instructions().replace('{', '{{').replace('}', '}}')

# Build all chains
problem_chain = build_problem_prompt(_score_instructions) | llm | score_reason_parser
product_diff_chain = build_product_diff_prompt(_score_instructions) | llm | score_reason_parser
bm_chain = build_business_model_prompt(_score_instructions) | llm | score_reason_parser
market_chain = build_market_prompt(_score_instructions) | llm | score_reason_parser
revenue_chain = build_revenue_prompt(_score_instructions) | llm | score_reason_parser
competition_chain = build_competition_prompt(_score_instructions) | llm | score_reason_parser
structure_chain = build_structure_prompt(_structure_instructions) | llm | structure_parser
viability_chain = build_viability_prompt(_viability_instructions) | llm | viability_parser

# Parallel dimensions evaluation
dimensions_parallel = RunnableParallel(
    problem_clarity=problem_chain,
    product_differentiation=product_diff_chain,
    business_model_strength=bm_chain,
    market_opportunity=market_chain,
    revenue_logic=revenue_chain,
    competition_awareness=competition_chain,
    pitch_structure=structure_chain,
)


def analyze_pitch_with_viability(transcript: str) -> Dict:
    """
    1) Runs all dimension chains + pitch structure in parallel.
    2) Feeds results + transcript into business viability LLM.
    3) Returns a combined dict.
    """
    # 1) Parallel dimension evaluation
    dim_results = dimensions_parallel.invoke({"transcript": transcript})

    # 2) Convert Pydantic objects to dicts
    dim_scores_dict = {
        "problem_clarity": dim_results["problem_clarity"].model_dump(),
        "product_differentiation": dim_results["product_differentiation"].model_dump(),
        "business_model_strength": dim_results["business_model_strength"].model_dump(),
        "market_opportunity": dim_results["market_opportunity"].model_dump(),
        "revenue_logic": dim_results["revenue_logic"].model_dump(),
        "competition_awareness": dim_results["competition_awareness"].model_dump(),
    }
    pitch_structure_dict = dim_results["pitch_structure"].model_dump()

    # 3) JSON strings for viability prompt
    dimension_scores_json = json.dumps(dim_scores_dict, ensure_ascii=False, indent=2)
    pitch_structure_json = json.dumps(pitch_structure_dict, ensure_ascii=False, indent=2)

    # 4) Business viability (second stage)
    # Note: The viability_chain is designed to accept these as plain text
    viability_result = viability_chain.invoke(
        {
            "transcript": transcript,
            "dimension_scores": dimension_scores_json,
            "pitch_structure": pitch_structure_json,
        }
    )

    # 5) Combine everything
    final = {
        "dimensions": dim_scores_dict,
        "pitch_structure": pitch_structure_dict,
        "business_viability": viability_result.model_dump(),
    }
    return final


if __name__ == "__main__":
    # quick manual test
    import sys

    if len(sys.argv) > 1:
        transcript_file = sys.argv[1]
        with open(transcript_file, "r", encoding="utf-8") as f:
            text = f.read()
        print(json.dumps(analyze_pitch_with_viability(text), indent=2))
