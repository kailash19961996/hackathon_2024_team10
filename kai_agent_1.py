# Agent 1

from uagents import Agent, Bureau, Context, Model
from transformers import pipeline

# Initialize the Hugging Face NLP pipeline
nlp = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Define the Message model
class DocumentMessage(Model):
    text: str

class ResponseMessage(Model):
    rules: list

# Create the Document Parsing Agent
class DocumentParseAgent(Agent):
    def __init__(self, name: str, seed: str):
        super().__init__(name=name, seed=seed)

    @Agent.on_start
    async def on_start(self, ctx: Context):
        self.logger.info("Document Parsing Agent started")

    @Agent.on_message(model=DocumentMessage)
    async def on_parse_document(self, ctx: Context, sender: str, msg: DocumentMessage):
        document_text = msg.text
        if document_text:
            rules = self.generate_rules(document_text)
            await ctx.send(sender, ResponseMessage(rules=rules))
        else:
            await ctx.send(sender, ResponseMessage(rules=["No document text provided"]))

    def generate_rules(self, document_text):
        # Preprocess the document text (if needed)
        preprocessed_text = document_text.strip()

        # Use the Hugging Face pipeline to classify the document text
        result = nlp(preprocessed_text)[0]

        # Extract the label from the classification result
        label = result["label"]

        # Generate rules based on the label
        if label == "POSITIVE":
            rules = ["Allow the requested action", "Grant access"]
        elif label == "NEGATIVE":
            rules = ["Deny the requested action", "Restrict access"]
        else:
            rules = ["Further review needed"]

        return rules

# Create the Requesting Agent
class RequestingAgent(Agent):
    def __init__(self, name: str, seed: str):
        super().__init__(name=name, seed=seed)

    @Agent.on_interval(period=3.0)
    async def send_message(self, ctx: Context):
        document_text = "This is a sample document text to classify."
        await ctx.send(parsing_agent.address, DocumentMessage(text=document_text))

    @Agent.on_message(model=ResponseMessage)
    async def handle_response(self, ctx: Context, sender: str, msg: ResponseMessage):
        ctx.logger.info(f"Received rules from {sender}: {msg.rules}")

# Initialize the agents
parsing_agent = DocumentParseAgent(name="document_parser", seed="parser recovery phrase")
requesting_agent = RequestingAgent(name="requester", seed="requester recovery phrase")

# Initialize the Bureau
bureau = Bureau()
bureau.add(parsing_agent)
bureau.add(requesting_agent)

# Run the Bureau
if __name__ == "__main__":
    bureau.run()
