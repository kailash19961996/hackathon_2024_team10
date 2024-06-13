import os
import json
import openai
import logging
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
openai.api_key = api_key
print("---------api_key_works---------")

class Rule(Model):
    rules: str

class Claim(Model):
    claim: str

# Agent3 setup
agent3 = Agent(name="agent3", port=8014, seed="agent3 secret phrase", endpoint=["http://127.0.0.1:8014/submit"], mailbox="723cb337-1e2f-4f0f-8e92-5a18873962d3@agentverse.ai")
print("uAgent address: ", agent3.address)  # This needs to be used for the recipient_address in agent1
# print("Fetch network address: ", agent3.wallet.address())

# Fund the agent if low
fund_agent_if_low(agent3.wallet.address())

rules_text = None
claims_text = None

@agent3.on_message(model=Rule)
async def handle_rules(ctx: Context, sender: str, msg: Rule):
    global rules_text
    try:
        rules_text = msg.rules
        ctx.logger.info(f"Received rules text: \n\n{rules_text}")
        await process_data(ctx)
    except Exception as e:
        ctx.logger.error(f"Failed to process rules text: {e}")

@agent3.on_message(model=Claim)
async def handle_claims(ctx: Context, sender: str, msg: Claim):
    global claims_text
    try:
        claims_text = msg.claim
        ctx.logger.info(f"Received claims text: \n\n{claims_text}")
        await process_data(ctx)
    except Exception as e:
        ctx.logger.error(f"Failed to process claims text: {e}")


def parse_rules(text):
    rules = [line.strip() for line in text.strip().split('\n') if line.strip()]
    return rules

def parse_claim(text):
    claim = [line.strip() for line in text.strip().split('\n') if line.strip()]
    return claim

async def find_relevant_rule(claim, rules):
    prompt = (
        "Given the following insurance claim {claim} and set of rules {rules}, find the most relevant rule and price range for the claim.\n\n"
        f"Claim: {claim}\n\n"
        "Rules:\n" + "\n".join(rules) + "\n\n"
        "Relevant rule:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2000,
        temperature=0.5
    )
    return response.choices[0].message['content'].strip()


async def process_data(ctx):
    global rules_text, claims_text
    if rules_text and claims_text:
        try:
            # Parse rules and claim
            rules = parse_rules(rules_text)
            print(f"\nThe len of rules is {len(rules)}")
            user_claim = parse_claim(claims_text)
            print(f"The len of user_claim is {len(user_claim)}")
            print(f"\nuser_claim[0] - {user_claim[0]}")

            # Find the most relevant rule using GPT-4
            relevant_rule = await find_relevant_rule(user_claim[0], rules)
            
            ctx.logger.info(f"Most relevant rule found: \n\n{relevant_rule}")
            
            result = {"claim status": "claim approved",
                      "relevant_rule": relevant_rule}

            # Save prediction to JSON
            with open("price_prediction.json", "w") as f:
                json.dump(result, f)
            
        except KeyError as e:
            ctx.logger.error(f"Key error during processing: {e}")
        except Exception as e:
            ctx.logger.error(f"Unexpected error during processing: {e}")
    else:
        ctx.logger.debug("Rules or claims are not yet set")

if __name__ == "__main__":
    agent3.run()


# Model outputs- 1

# Given Irrelevant document
# user_claim[0] user_id: 12345, name: John Doe, request: early retirement, age: 58, ill_health: yes, current_pension: $2500, join_date: June 15, 1990, spouse_eligible: yes
# INFO:     [agent3]: Most relevant rule found: The provided claim does not relate to travel insurance but rather seems to be a claim for early retirement due to ill health. The set of rules provided are all related to travel insurance coverage, and none of them are directly relevant to an early retirement claim. 
# However, if we were to find the most relevant rule from the given set for the claim, we must acknowledge that none of the rules directly apply. The claim involves specifics about retirement, health status, pension, and spouse eligibility, which are not covered by the travel insurance rules provided.
# In conclusion, there is no relevant rule from the provided set of travel insurance rules that applies to the early retirement claim. Therefore, no price range can be determined from the given rules for this claim.



# Model outputs- 2

# Given relevant document
# Picks the right one

# user_claim[0] user_id: 12345, name: John Doe, request: early retirement, age: 58, ill_health: yes, current_pension: $2500, join_date: June 15, 1990, spouse_eligible: yes
# INFO:     [agent3]: Most relevant rule found: Based on the provided claim and rules, the most relevant rule for John Doe's insurance claim is:

# **Rule 1: Early Retirement Eligibility**

# ### Justification:
# - **Age**: John Doe is 58 years old, which is below the standard retirement age.
# - **Health**: John Doe is in bad health.
# - **Request**: John Doe is requesting early retirement.

# ### Approximate Price Range:
# The approximate price range for early retirement as per Rule 1 is **$2000 - $3000 per month**.

# Additionally, since John Doe's spouse is eligible for benefits, Rule 3 also applies:
# - **Spousal Benefits Eligibility**: The approximate price range for spousal benefits is **$500 - $1000 per month**.

# Combining both relevant rules, John Doe's total pension amount may be influenced by both the early retirement eligibility and spousal benefits eligibility. However, the primary relevant rule for the claim is Rule 1: Early Retirement Eligibility.
