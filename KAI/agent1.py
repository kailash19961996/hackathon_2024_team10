# agent1.py
from uagents import Agent, Context
from transformers import pipeline
from message_models import DocumentAMessage, RulesMessage
import fitz  # PyMuPDF

# Initialize the summarization pipeline
nlp_summarization = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

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
            await ctx.send(sender, RulesMessage(rules=rules))
        else:
            await ctx.send(sender, RulesMessage(rules=["No document text provided"]))

    def generate_rules(self, document_text):
        preprocessed_text = document_text.strip()
        result = nlp_summarization(preprocessed_text, max_length=512, min_length=30, do_sample=False)
        rules = [summary['summary_text'] for summary in result]
        return rules

# Initialize and run Agent1
agent1 = Agent1(name="agent1", seed="agent1 recovery phrase")

if __name__ == "__main__":
    agent1.run(port=8001)
