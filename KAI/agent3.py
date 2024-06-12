# agent3.py
from uagents import Agent, Context
from message_models import RulesMessage, ClaimDetailsMessage, PredictionMessage

class Agent3(Agent):
    def __init__(self, name: str, seed: str):
        super().__init__(name=name, seed=seed)
        self.rules = []
        self.details = []

    @Agent.on_start
    async def on_start(self, ctx: Context):
        self.logger.info("Agent 3 started")

    @Agent.on_message(model=RulesMessage)
    async def on_receive_rules(self, ctx: Context, sender: str, msg: RulesMessage):
        self.rules = msg.rules
        self.check_and_predict(ctx)

    @Agent.on_message(model=ClaimDetailsMessage)
    async def on_receive_details(self, ctx: Context, sender: str, msg: ClaimDetailsMessage):
        self.details = msg.details
        self.check_and_predict(ctx)

    def check_and_predict(self, ctx: Context):
        if self.rules and self.details:
            prediction = self.generate_prediction(self.rules, self.details)
            ctx.logger.info(f"Generated prediction: {prediction}")
            print(f"Generated prediction: {prediction}")

    def generate_prediction(self, rules, details):
        # Here you can implement your logic to combine rules and details and generate a prediction.
        # For demonstration, we simply concatenate the rules and details.
        return f"Prediction based on rules: {rules} and details: {details}"

# Initialize and run Agent3
agent3 = Agent3(name="agent3", seed="agent3 recovery phrase")

if __name__ == "__main__":
    agent3.run(port=8003)
