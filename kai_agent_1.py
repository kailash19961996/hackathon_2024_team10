from uagents import Agent, Protocol, Message, Context
from transformers import pipeline

# Initialize the Hugging Face NLP pipeline
nlp = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Define the protocol for agent communication
class DocumentParseProtocol(Protocol):
    def __init__(self):
        super().__init__(
            "document_parse",
            version="1.0.0",
            roles=("requester", "responder"),
            init_messages=(),
            messages=(Message("parse_document"),)
        )

# Create the Document Parsing Agent
class DocumentParseAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name, protocols=[DocumentParseProtocol()])

    async def on_start(self, ctx: Context):
        self.logger.info("Document Parsing Agent started")

    async def on_parse_document(self, ctx: Context, sender: str, message: Message):
        document_text = message.body.get("text")
        if document_text:
            rules = self.generate_rules(document_text)
            ctx.send(sender, "parsed_document", {"rules": rules})
        else:
            ctx.send(sender, "error", {"message": "No document text provided"})

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

# Create and run the agent
agent = DocumentParseAgent(name="document_parser")
agent.run()