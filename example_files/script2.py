import asyncio
import logging
import os
from uagents import Agent, Context, Model

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_key = os.getenv("AV_API_KEY", "")

async def analyze_data(data: str):
    analyzed_data = data.upper()  # Example: convert data to uppercase
    return analyzed_data

class DataScraped(Model):
    data: str

class DataAnalyzed(Model):
    analyzed_data: str

async def agent_function(ctx: Context, message: DataScraped):
    analyzed_data = await analyze_data(message.data)
    await ctx.send("combiner_agent", DataAnalyzed(analyzed_data=analyzed_data))

if __name__ == '__main__':
    agent = Agent(name="analyzer_agent")

    @agent.on_message(model=DataScraped)
    async def handle_message(ctx: Context, message: DataScraped):
        await agent_function(ctx, message)

    agent.run()
