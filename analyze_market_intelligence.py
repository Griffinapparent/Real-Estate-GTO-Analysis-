import json
import openai

# Set your OpenAI key
openai.api_key = "your-openai-api-key"


def load_property_data(filename="mock_properties.json"):
    with open(filename, "r") as f:
        return json.load(f)


def analyze_market_intelligence(properties, depth="advanced", timeframe="12m"):
    system_prompt = (
        "You are an expert real estate strategist. Analyze the following property data to extract competitor behavior, "
        "market dynamics, and strategic investment recommendations using game theory principles."
    )

    analysis_prompt = f"""
Analyze the following data from NYC commercial property transactions. Extract:
1. Most active investors and acquisition patterns
2. Bidding and pricing behavior
3. Market concentration and timing strategies
4. Strategic insights for investment timing, competitive entry, and defensive positioning
5. Risks and potential threats

Analysis depth: {depth}
Timeframe: {timeframe}

Property Data:
{json.dumps(properties[:10], indent=2)}

Format the output in clean sections with bullet points and key insights.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": analysis_prompt}
        ],
        temperature=0.3,
        max_tokens=3000
    )

    return response.choices[0].message["content"]


if __name__ == "__main__":
    data = load_property_data()
    analysis = analyze_market_intelligence(data)

    with open("market_analysis.txt", "w") as f:
        f.write(analysis)

    print("✅ Market analysis saved to market_analysis.txt")
