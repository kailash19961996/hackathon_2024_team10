import asyncio
import logging
import os
from uagents import Agent, Context, Model

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_key = os.getenv("AV_API_KEY", "")
output_file_path = 'combined_data.txt'

async def combine_and_store_data(data1: str, data2: str):
    combined_data = data1 + "\n\n" + data2
    with open(output_file_path, 'w') as f:
        f.write(combined_data)
    logger.info(f'Data combined and saved to {output_file_path}')

class DataAnalyzed(Model):
    analyzed_data: str

class DataScraped(Model):
    data: str

class DataStored(Model):
    message: str

async def agent_function(ctx: Context, message1: DataScraped, message2: DataAnalyzed):
    await combine_and_store_data(message1.data, message2.analyzed_data)
    await ctx.send("scraper_agent", DataStored(message="Data successfully combined and stored"))

if __name__ == '__main__':
    agent = Agent(name="combiner_agent")

    @agent.on_message(model=DataAnalyzed)
    async def handle_analyzed_message(ctx: Context, message: DataAnalyzed):
        message1 = await ctx.receive("DataScraped")
        await agent_function(ctx, message1, message)

    agent.run()
