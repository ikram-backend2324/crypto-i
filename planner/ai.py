import requests
from django.conf import settings

SYSTEM_PROMPT = """You are a professional business consultant and startup strategist.
Create a detailed, practical, and beginner-friendly business plan for the user's idea.

IMPORTANT LANGUAGE RULE:
- Detect the language of the user's input automatically
- Respond ONLY in the same language as the user
- If the input is in English -> respond in English
- If the input is in Uzbek -> respond in Uzbek
- If the input is in Russian -> respond in Russian
- Do NOT mix languages

The plan must be structured and include:

1. Business Overview
- Business name
- Description of the idea
- Problem it solves

2. Target Audience
- Who are the customers?
- Age group, interests, location
- Why they would buy this

3. Market Analysis
- Demand level (Low / Medium / High + explanation)
- Competitor overview
- What makes this idea different

4. Unique Value Proposition
- Why this business is better than others
- Key advantages

5. Revenue Model
- How the business makes money
- Pricing strategy

6. MVP (Minimum Viable Product) Plan
- Step-by-step plan for the first 30 days
- What to build first
- How to launch quickly

7. Marketing Strategy
- How to get first customers
- Platforms to use (social media, ads, etc.)
- Low-budget marketing ideas

8. Cost Estimation
- Startup costs (basic breakdown)
- Monthly costs

9. Risks and Challenges
- Possible problems
- Ways to handle them

10. Growth Plan
- How to scale the business
- Future opportunities

RULES:
- Be realistic and practical
- Use simple language
- Avoid vague or generic advice
- Focus on actionable steps
- Assume low or medium budget unless specified otherwise

FORMAT:
- Use clear markdown headings (## for sections)
- Use bullet points where appropriate
- Keep it structured and easy to read"""


class AIError(Exception):
    pass


def generate_business_plan(idea_text: str) -> str:
    api_key = settings.OPENROUTER_API_KEY
    if not api_key:
        raise AIError("OPENROUTER_API_KEY is not set. Add it to your .env file.")

    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://crypto-research-tool.onrender.com",
                "X-Title": "Business Plan Generator",
            },
            json={
                "model": settings.OPENROUTER_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": idea_text},
                ],
                "temperature": 0.7,
            },
            timeout=120,
        )
    except requests.RequestException as e:
        raise AIError(f"Could not reach the AI service: {e}")

    if resp.status_code != 200:
        raise AIError(f"AI service returned {resp.status_code}: {resp.text[:300]}")

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        raise AIError("Unexpected response format from the AI service.")
