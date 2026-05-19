import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

ALPHA_PROMPT = """You are AXIOM Alpha — the analytical and logical agent of the AXIOM system built by Robair Farag.
You think in data, facts, and systems. You are precise, direct, and evidence-based.
Keep your response to 2-3 sentences maximum. No formatting. Speak naturally.
Always start with 'Alpha:' """

BETA_PROMPT = """You are AXIOM Beta — the creative and unconventional agent of the AXIOM system built by Robair Farag.
You think outside the box, challenge assumptions, and find unexpected angles.
Keep your response to 2-3 sentences maximum. No formatting. Speak naturally.
Always start with 'Beta:' """

GAMMA_PROMPT = """You are AXIOM Gamma — the critical and skeptical agent of the AXIOM system built by Robair Farag.
You find flaws, risks, and weaknesses in any argument. You play devil's advocate.
Keep your response to 2-3 sentences maximum. No formatting. Speak naturally.
Always start with 'Gamma:' """

SYNTHESIS_PROMPT = """You are AXIOM, the unified intelligence built by Robair Farag.
Three of your sub-agents just debated a question. Synthesize their views into one final answer.
Keep it to 2-3 sentences. Natural, human, conversational. No formatting.
Address the user as Sir."""

def multi_agent_debate(question):
    """Run a multi-agent debate and return all responses"""
    results = {}

    # Alpha responds
    alpha_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        system=ALPHA_PROMPT,
        messages=[{"role": "user", "content": question}]
    )
    results['alpha'] = alpha_response.content[0].text

    # Beta responds
    beta_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        system=BETA_PROMPT,
        messages=[{"role": "user", "content": question}]
    )
    results['beta'] = beta_response.content[0].text

    # Gamma responds with awareness of Alpha and Beta
    gamma_context = f"Question: {question}\n\nAlpha said: {results['alpha']}\nBeta said: {results['beta']}\n\nNow give your critical perspective."
    gamma_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        system=GAMMA_PROMPT,
        messages=[{"role": "user", "content": gamma_context}]
    )
    results['gamma'] = gamma_response.content[0].text

    # Final synthesis
    synthesis_context = f"""Question asked: {question}

Alpha (analytical): {results['alpha']}
Beta (creative): {results['beta']}
Gamma (critical): {results['gamma']}

Now synthesize these three perspectives into your final unified answer."""

    synthesis_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        system=SYNTHESIS_PROMPT,
        messages=[{"role": "user", "content": synthesis_context}]
    )
    results['synthesis'] = synthesis_response.content[0].text

    return results
