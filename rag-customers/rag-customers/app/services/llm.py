from openai import OpenAI

async def generate_answer(prompt, context):
    model = "gpt-4o-mini"
    response = await OpenAI.Completion.create(
        model=model,
        prompt=f"{context}\n\n{prompt}",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()