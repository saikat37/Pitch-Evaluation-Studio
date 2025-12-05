"""Centralized prompt templates for content evaluation chains.
All prompts include few-shot examples from athena(1).py
"""
from langchain_core.prompts import ChatPromptTemplate


def build_problem_prompt(format_instructions: str) -> ChatPromptTemplate:
    """Problem clarity evaluation with few-shot examples."""
    return ChatPromptTemplate.from_messages([
        ("system",
         "You are a VC and pitch coach. Your ONLY task is to evaluate "
         "'problem clarity' in a startup pitch transcript.\n"
         "- Score must be between 0 and 100 (int).\n"
         "- Reason must briefly explain why.\n"
         "Do NOT evaluate any other dimension.\n\n"
         f"{format_instructions}"),
        ("user",
         "TRANSCRIPT:\n"
         "Hi Sharks, today small grocery shop owners lose hours every week manually "
         "writing bills and tracking credit in notebooks. They often misplace records "
         "and lose up to 10% of revenue due to errors.\n"),
        ("assistant",
         '{{\"score\": 90, \"reason\": \"The problem is very clear: who is affected (small shop owners), what happens (manual bookkeeping), and the consequence (lost time and revenue).\"}}'),
        ("user",
         "TRANSCRIPT:\n"
         "So yeah, things are kind of messy in this space and people don't have great tools.\n"),
        ("assistant",
         '{{\"score\": 40, \"reason\": \"The problem is vague: the speaker says things are messy but does not specify who is affected or what the concrete problem is.\"}}'),
        ("user",
         "TRANSCRIPT:\n{transcript}\n\n"
         "Now evaluate ONLY 'problem clarity' as in the examples above."),
    ])


def build_product_diff_prompt(format_instructions: str) -> ChatPromptTemplate:
    """Product differentiation evaluation with few-shot examples."""
    return ChatPromptTemplate.from_messages([
        ("system",
         "You are a VC and pitch coach. Your ONLY task is to evaluate "
         "'product differentiation' in a startup pitch transcript.\n"
         "Interpret this as: how clearly and concretely the founder explains what makes "
         "their product different or better than existing solutions or the status quo.\n"
         "Output MUST follow the given JSON schema and keep score between 0 and 100.\n"
         f"{format_instructions}"),
        ("user",
         "TRANSCRIPT:\n"
         "Today, restaurants use Excel and WhatsApp to manage suppliers. Our product is a single "
         "dashboard that automatically syncs orders, invoices, and inventory in real time, unlike "
         "existing tools which are manual.\n"),
        ("assistant",
         '{{"score": 88, "reason": "The founder explicitly compares their product with Excel and WhatsApp and explains the unique benefit: automatic, real-time syncing versus manual tools."}}'),
        ("user",
         "TRANSCRIPT:\n"
         "Our app is unique and better than anything out there.\n"),
        ("assistant",
         '{{"score": 45, "reason": "The founder claims uniqueness but provides no concrete comparison or explanation of what is different."}}'),
        ("user",
         "TRANSCRIPT:\n{transcript}\n\n"
         "Now evaluate ONLY 'product differentiation' as in the examples above."),
    ])


def build_business_model_prompt(format_instructions: str) -> ChatPromptTemplate:
    """Business model strength evaluation."""
    return ChatPromptTemplate.from_messages([
        ("system",
         "You are a VC and pitch coach. Evaluate ONLY 'business model strength' in "
         "the transcript.\n"
         "Focus on whether they clearly explain who pays, what they pay for, and how often.\n"
         f"Output MUST follow the JSON schema and keep score 0–100.\n{format_instructions}"),
        ("user",
         "TRANSCRIPT:\n"
         "We charge small clinics a monthly subscription of $99 per doctor. They pay us directly "
         "for our practice management software.\n"),
        ("assistant",
         '{{"score": 90, "reason": "The model is clearly defined: who pays (small clinics), how much ($99/doctor), and how often (monthly)."}}'),
        ("user",
         "TRANSCRIPT:\n"
         "We will figure out monetization later once we have users.\n"),
        ("assistant",
         '{{"score": 20, "reason": "The founder explicitly defers monetization and does not provide a current business model."}}'),
        ("user",
         "TRANSCRIPT:\n{transcript}\n\n"
         "Now evaluate ONLY 'business model strength' as in the examples above."),
    ])


def build_market_prompt(format_instructions: str) -> ChatPromptTemplate:
    """Market opportunity articulation."""
    return ChatPromptTemplate.from_messages([
        ("system",
         "You are a VC and pitch coach. Evaluate ONLY 'market opportunity articulation'.\n"
         f"Look for market size, growth, or urgency.\nOutput MUST follow the JSON schema and keep score 0–100.\n{format_instructions}"),
        ("user",
         "TRANSCRIPT:\n"
         "We are targeting the $10B global pet care market, growing at 12% annually.\n"),
        ("assistant",
         '{{\"score\": 92, \"reason\": \"The founder mentions a specific market size and growth rate, making the opportunity clear.\"}}'),
        ("user",
         "TRANSCRIPT:\n"
         "This is a huge space with a lot of potential.\n"),
        ("assistant",
         '{{"score": 50, "reason": "The founder claims the market is huge but provides no numbers or specifics."}}'),
        ("user",
         "TRANSCRIPT:\n{transcript}\n\n"
         "Evaluate ONLY 'market opportunity articulation' as in the examples above."),
    ])


def build_revenue_prompt(format_instructions: str) -> ChatPromptTemplate:
    """Revenue logic evaluation."""
    return ChatPromptTemplate.from_messages([
        ("system",
         "You are a VC and pitch coach. Evaluate ONLY 'revenue logic'.\n"
         "Judge whether the way they make money is logically consistent with the product, "
         f"target customer, and problem.\nOutput MUST follow the JSON schema and keep score 0–100.\n{format_instructions}"),
        ("user",
         "TRANSCRIPT:\n"
         "We take a 5% commission on every transaction between hotels and suppliers on our platform.\n"),
        ("assistant",
         '{{"score": 85, "reason": "The commission-based revenue aligns with a marketplace model connecting hotels and suppliers."}}'),
        ("user",
         "TRANSCRIPT:\n"
         "We solve problems for poor farmers, and they will pay us $1000 per month.\n"),
        ("assistant",
         '{{"score": 35, "reason": "Charging poor farmers $1000 per month seems unrealistic and misaligned with their ability to pay."}}'),
        ("user",
         "TRANSCRIPT:\n{transcript}\n\n"
         "Evaluate ONLY 'revenue logic' as in the examples above."),
    ])


def build_competition_prompt(format_instructions: str) -> ChatPromptTemplate:
    """Competition awareness evaluation."""
    return ChatPromptTemplate.from_messages([
        ("system",
         "You are a VC and pitch coach. Evaluate ONLY 'competition awareness'.\n"
         f"Check if they mention existing competitors, tools, or status quo.\nOutput MUST follow the JSON schema and keep score 0–100.\n{format_instructions}"),
        ("user",
         "TRANSCRIPT:\n"
         "Today, companies use tools like Salesforce and HubSpot. "
         "We integrate with them but focus only on after-sales support.\n"),
        ("assistant",
         '{{"score": 88, "reason": "The founder names major incumbents and explains how they position themselves relative to them."}}'),
        ("user",
         "TRANSCRIPT:\n"
         "We don't really have competitors because no one does what we do.\n"),
        ("assistant",
         '{{"score": 40, "reason": "Claiming there are no competitors suggests a lack of realism about alternatives or status quo."}}'),
        ("user",
         "TRANSCRIPT:\n{transcript}\n\n"
         "Evaluate ONLY 'competition awareness' as in the examples above."),
    ])


def build_structure_prompt(format_instructions: str) -> ChatPromptTemplate:
    """Pitch structure detection."""
    return ChatPromptTemplate.from_messages([
        ("system",
         "You are a pitch coach. Detect if the transcript follows a clear structure: "
         "Hook → Problem → Solution → Ask.\n"
         f"Return JSON with booleans, detected_order, and structure_quality_score (0–100).\n{format_instructions}"),
        ("user",
         "TRANSCRIPT:\nHi, we have a problem. Our solution is great. Please invest.\n\n"
         "Identify whether a hook, problem, solution, and ask are present, and in which order."),
        ("assistant",
         '{{\"hook_present\": true, \"problem_present\": true, \"solution_present\": true, \"ask_present\": true, \"detected_order\": [\"hook\", \"problem\", \"solution\", \"ask\"], \"structure_quality_score\": 90, \"structure_comment\": \"The pitch clearly presents all key structural elements in the expected order.\"}}'),
        ("user",
         "TRANSCRIPT:\n{transcript}\n\n"
         "Identify whether a hook, problem, solution, and ask are present, and in which order."),
    ])


def build_viability_prompt(format_instructions: str) -> ChatPromptTemplate:
    """Business viability analysis (2nd stage)."""
    from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
    from langchain_core.prompts.string import DEFAULT_FORMATTER_MAPPING, StringPromptTemplate
    
    # Create a custom template that doesn't parse variables in the content
    system_msg = SystemMessagePromptTemplate.from_template(
        "You are a venture capitalist evaluating an early-stage startup pitch.\n"
        "You receive:\n"
        "1) The full transcript of the pitch.\n"
        "2) Pre-computed scores for problem_clarity, product_differentiation, business_model_strength, market_opportunity, revenue_logic, competition_awareness\n"
        "3) A pitch_structure analysis (hook, problem, solution, ask, and order).\n\n"
        "Your job is to generate a JSON object evaluating business viability.\n"
        "Return ONLY valid JSON with NO additional text, markdown, or wrapping.\n"
        "The JSON must contain these exact fields at the root level:\n"
        "- score (integer 0-100)\n"
        "- risk_level (string: 'low', 'medium', or 'high')\n"
        "- summary_comment (string)\n"
        "- key_strengths (array of strings)\n"
        "- key_risks (array of strings)\n\n"
        f"{format_instructions}",
        template_format="f-string"
    )
    
    # User messages with f-string format to avoid brace interpretation
    return ChatPromptTemplate.from_messages([
        system_msg,
        ("user",
         "TRANSCRIPT:\nWe solve a clear problem with a unique product.\n\n"
         'DIMENSION_SCORES:\n{{"problem_clarity": {{"score": 85}}}}\n\n'
         'PITCH_STRUCTURE:\n{{"structure_quality_score": 80}}\n\n'
         "Generate the business viability analysis."),
        ("assistant",
         '{{"score": 75, "risk_level": "medium", "summary_comment": "Solid problem clarity but limited business model details.", "key_strengths": ["Clear problem statement"], "key_risks": ["Unclear monetization"]}}'),
        HumanMessagePromptTemplate.from_template(
            "TRANSCRIPT:\n{transcript}\n\n"
            "DIMENSION_SCORES (JSON):\n{dimension_scores}\n\n"
            "PITCH_STRUCTURE (JSON):\n{pitch_structure}\n\n"
            "Generate the business viability analysis as a JSON object with the exact fields specified. Return ONLY the JSON object, no other text.",
            template_format="f-string"
        ),
    ])


__all__ = [
    "build_problem_prompt",
    "build_product_diff_prompt",
    "build_business_model_prompt",
    "build_market_prompt",
    "build_revenue_prompt",
    "build_competition_prompt",
    "build_structure_prompt",
    "build_viability_prompt",
]
