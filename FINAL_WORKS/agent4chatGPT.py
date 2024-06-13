# Vector search

import os
import json
import numpy as np
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

class Rule(Model):
    rules: str

class Claim(Model):
    claim: str

# agent4 setup
agent4 = Agent(name="agent4", port=8013, seed="agent4 secret phrase", endpoint=["http://127.0.0.1:8013/submit"])
print("uAgent address: ", agent4.address)  # This needs to be used for the recipient_address in agent1
# print("Fetch network address: ", agent4.wallet.address())

# Fund the agent if low
fund_agent_if_low(agent4.wallet.address())

rules_text = None
claims_text = None

@agent4.on_message(model=Rule)
async def handle_rules(ctx: Context, sender: str, msg: Rule):
    global rules_text
    try:
        rules_text = msg.rules
        ctx.logger.info(f"Received rules text: {rules_text}")
        await process_data(ctx)
    except Exception as e:
        ctx.logger.error(f"Failed to process rules text: {e}")

@agent4.on_message(model=Claim)
async def handle_claims(ctx: Context, sender: str, msg: Claim):
    global claims_text
    try:
        claims_text = msg.claim
        ctx.logger.info(f"Received claims text: {claims_text}")
        await process_data(ctx)
    except Exception as e:
        ctx.logger.error(f"Failed to process claims text: {e}")

def parse_rules(text):
    rules = [line.strip() for line in text.strip().split('\n') if line.strip()]
    return rules

def parse_claim(text):
    claim = [line.strip() for line in text.strip().split('\n') if line.strip()]
    return claim

def vector_search(user_claim, rules):
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit and transform rules
    rule_vectors = vectorizer.fit_transform(rules)
    
    # Transform user claim
    claim_vector = vectorizer.transform([user_claim])
    
    # Compute cosine similarities
    similarities = cosine_similarity(claim_vector, rule_vectors)
    
    # Get index of most similar rule
    most_similar_index = np.argmax(similarities)
    
    # Return most similar rule
    return rules[most_similar_index]

async def process_data(ctx):
    global rules_text, claims_text
    if rules_text and claims_text:
        try:
            # Parse rules and claim
            rules = parse_rules(rules_text)
            print(f"\nThe len of rules is {len(rules)}")
            user_claim = parse_claim(claims_text)
            print(f"The len of user_claim is {len(user_claim)}")
            print(f"\n user_claim[0]{user_claim[0]}")

            # Find most relevant rule using vector search
            relevant_rule = vector_search(user_claim[0], rules)
            
            ctx.logger.info(f"Most relevant rule found: {relevant_rule}")
            
            ctx.logger.info(f"Price prediction: {"claim approved"}")

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
    agent4.run()


# Model outputs- 1

# The len of user_claim is 2
# user_claim[0] user_id: 12345, name: John Doe, request: early retirement, age: 58, ill_health: yes, current_pension: $2500, join_date: June 15, 1990, spouse_eligible: yes
# INFO:     [agent4]: Most relevant rule found: 6. **Commutation available?:** Yes, where possible.
# INFO:     [agent4]: Price prediction: claim approved


# Model outputs- 2
# The len of user_claim is 2
# user_claim[0]user_id: 12345, name: John Doe, request: early retirement, age: 58, ill_health: yes, current_pension: $2500, join_date: June 15, 1990, spouse_eligible: yes
# INFO:     [agent4]: Most relevant rule found: 8. **Commutation Available**: Yes – maximum allowable under post 5 April 2006 legislation. (Price Range: $50 - $200)
# INFO:     [agent4]: Price prediction: claim approved




# Findings
# 1. vector search finds the information, but not very wise as is doesnt understand the context
# 2. sometime the agent 1 creates a file with the pricing information on the same line, then agent 3 prints out the suggested price as well. The work around is to ask the model to create the rules and suggested prices in one line.

# JSON output
# {"claim status": "claim approved", "relevant_rule": "5.6 **Commutation available?**: Yes, where possible."}