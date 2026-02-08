from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from ..schemas.state import CountOutput

# client = AsyncOpenAI(
#     base_url='http://localhost:11434/v1',
#     api_key='ollama'
# )

model = OpenAIChatModel(
            model_name='llama3.1', 
            provider=OpenAIProvider(
                base_url='http://localhost:11434/v1', 
                api_key='ollama'
            )
        )

counter_agent = Agent(
    model,          
    instructions="You are a smart and efficient word counter. Count words in the text.",
    output_type=CountOutput,
    system_prompt=(
        "Count the number of words in the text. "
        "IMPORTANT: You must respond ONLY with a JSON object. "
        "Do not include any introductory text or markdown code blocks."
    )
)
