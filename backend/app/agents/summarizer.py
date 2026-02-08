from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from ..schemas.state import SummaryOutput

# client = AsyncOpenAI(
#     base_url='http://localhost:11434/v1',
#     api_key='ollama',
# )

model = OpenAIChatModel(
            model_name='llama3.1', 
            provider=OpenAIProvider(
                base_url='http://localhost:11434/v1', 
                api_key='ollama'
            )
        )

summarizer_agent = Agent(model, 
                         instructions="You are a smart and efficient summarizer. Summarize the following text.", 
                         output_type=SummaryOutput,
                         system_prompt=(
                            "Summarize the text. "
                            "IMPORTANT: You must respond ONLY with a JSON object. "
                            "Do not include any introductory text or markdown code blocks."
                         )
                    )

#  result_type=CountOutput, system_prompt="Count words in the text."
