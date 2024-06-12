from uagents import Agent, Bureau, Context, Model
import fitz  # PyMuPDF
from transformers import pipeline

# Initialize the Hugging Face NLP pipelines
nlp_summarization = pipeline("summarization", model="facebook/bart-large-cnn")
nlp_ner = pipeline("ner", model="dslim/bert-base-NER")

# Define the Message models
class DocumentAMessage(Model):
    text: str

class DocumentBMessage(Model):
    text: str

class DocumentCMessage(Model):
    text: str

class RulesMessage(Model):
    rules: list

class ClaimDetailsMessage(Model):
    details: list

class PredictionMessage(Model):
    prediction: str

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Agent 1: Processes terms and conditions to create rules
class Agent1(Agent):
    def __init__(self, name: str, seed: str):
        super().__init__(name=name, seed=seed)

    @Agent.on_start
    async def on_start(self, ctx: Context):
        self.logger.info("Agent 1 started")

    @Agent.on_message(model=DocumentAMessage)
    async def on_parse_document_a(self, ctx: Context, sender: str, msg: DocumentAMessage):
        document_text = msg.text
        if document_text:
            rules = self.generate_rules(document_text)
            await ctx.send(agent3.address, RulesMessage(rules=rules))
        else:
            await ctx.send(agent3.address, RulesMessage(rules=["No document text provided"]))

    def generate_rules(self, document_text):
        preprocessed_text = document_text.strip()
        result = nlp_summarization(preprocessed_text, max_length=512, min_length=30, do_sample=False)
        rules = [summary['summary_text'] for summary in result]
        return rules

# Agent 2: Processes user claim details to extract relevant information
class Agent2(Agent):
    def __init__(self, name: str, seed: str):
        super().__init__(name=name, seed=seed)

    @Agent.on_start
    async def on_start(self, ctx: Context):
        self.logger.info("Agent 2 started")

    @Agent.on_message(model=DocumentCMessage)
    async def on_parse_document_c(self, ctx: Context, sender: str, msg: DocumentCMessage):
        document_text = msg.text
        if document_text:
            details = self.extract_details(document_text)
            await ctx.send(agent3.address, ClaimDetailsMessage(details=details))
        else:
            await ctx.send(agent3.address, ClaimDetailsMessage(details=["No document text provided"]))

    def extract_details(self, document_text):
        preprocessed_text = document_text.strip()
        result = nlp_ner(preprocessed_text)
        details = [entity['word'] for entity in result]
        return details

# Agent 3: Combines information from Agent1 and Agent2 and predicts the claim outcome
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

# Initialize the agents
agent1 = Agent1(name="agent1", seed="agent1 recovery phrase")
agent2 = Agent2(name="agent2", seed="agent2 recovery phrase")
agent3 = Agent3(name="agent3", seed="agent3 recovery phrase")

# Initialize the Bureau
bureau = Bureau()
bureau.add(agent1)
bureau.add(agent2)
bureau.add(agent3)

# Run the Bureau
if __name__ == "__main__":
    # Simulate sending documents to the agents
    document_a_path = "path/to/documentA.pdf"
    document_b_path = "path/to/documentB.pdf"
    document_c_path = "path/to/documentC.pdf"

    document_a_text = extract_text_from_pdf(document_a_path)
    document_b_text = extract_text_from_pdf(document_b_path)
    document_c_text = extract_text_from_pdf(document_c_path)

    # Start the bureau
    bureau.run()

    # Send messages to agents (simulating the process)
    agent1.send_message(agent1.address, DocumentAMessage(text=document_a_text))
    agent2.send_message(agent2.address, DocumentCMessage(text=document_c_text))
