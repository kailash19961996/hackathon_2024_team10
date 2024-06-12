import asyncio
import logging
import os
import sys
import aiohttp

from ai_engine_sdk import (
    AiEngine,
    is_agent_message,
    is_ai_engine_message,
    is_confirmation_message,
    is_stop_message,
    is_task_selection_message, TaskSelectionMessage
)
from ai_engine_sdk import ApiBaseMessage, FunctionGroup

logger = logging.getLogger(__name__)
api_key = os.getenv("AV_API_KEY", "")

if not api_key:
    raise Exception("API key is missing. Please set the AV_API_KEY environment variable.")


async def make_api_request(endpoint: str, params: dict = None, retries: int = 3):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    for attempt in range(retries):
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers, params=params) as response:
                response_text = await response.text()
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    raise Exception(f"Unauthorized request (status 401) to {endpoint}")
                else:
                    print(f"Attempt {attempt + 1} failed: {response.status} - {response_text}")
                    if attempt < retries - 1:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
    raise Exception(f"Failed to get a successful response from {endpoint} after {retries} attempts")


async def main():
    logger.debug("🚀 Starting example execution")
    ai_engine = AiEngine(api_key)

    try:
        function_groups: list[FunctionGroup] = await ai_engine.get_function_groups()
    except Exception as e:
        logger.error(f"Error fetching function groups: {e}")
        raise e

    public_group = next((g for g in function_groups if g.name == "Fetch Verified"), None)
    if public_group is None:
        raise Exception('Could not find "Public" function group.')

    session = await ai_engine.create_session(function_group=public_group.uuid)
    default_objective: str = "Find a flight to Warsaw."
    objective = input(f"What is your objective [default: {default_objective}]: ") or default_objective
    await session.start(objective)

    try:
        empty_count = 0
        session_ended = False

        while empty_count < 100:
            messages: list[ApiBaseMessage] = await session.get_messages()
            if len(messages) == 0:
                empty_count += 1
            else:
                empty_count = 0

            message: ApiBaseMessage
            for message in messages:
                if is_task_selection_message(message_type=message.type):
                    task_selection_message: TaskSelectionMessage = message
                    print("Please select an option from the list below:\n")
                    for _, option in task_selection_message.options.items():
                        print(f"{option.key}: {option.title}")

                    option_key = str(input("\nEnter task number: "))

                    if option_key not in task_selection_message.options.keys():
                        raise Exception("Invalid task number")

                    logger.debug(option_key)
                    await session.submit_task_selection(message, [task_selection_message.options[option_key]])
                    del task_selection_message
                elif is_agent_message(message):
                    print("Agent: ", message.text)

                    response = input("User (enter to skip): ")
                    if response == "exit":
                        break

                    if response != "":
                        await session.submit_response(message, response)
                elif is_ai_engine_message(message):
                    print("Engine:", message.text)
                elif is_confirmation_message(message_type=message.type):
                    print("Confirm:", message.payload)

                    response = input("\nPress enter to confirm, otherwise explain issue:\n")

                    if response == "":
                        await session.submit_confirmation(message)
                    else:
                        await session.reject_confirmation(message, response)
                elif is_stop_message(message):
                    print("\nSession has ended")
                    session_ended = True
                    break

            if session_ended:
                break

            await asyncio.sleep(1.5)
            logger.debug(f"No messages: {empty_count} times in a row")
    except Exception as e:
        logger.debug(f"Unhandled exception: {e}")
        print("Error", e)
        raise e
    finally:
        await session.delete()


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s',
    )
    asyncio.run(main())
