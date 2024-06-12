# agent2.py
from uagents import Agent, Context
from transformers import pipeline
from message_models import DocumentCMessage, ClaimDetailsMessage
import fitz  # PyMuPDF

# Initialize the NER pipeline
nlp_ner = pipeline("ner", model="dslim/bert-base-NER")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

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
            await ctx.send(sender, ClaimDetailsMessage(details=details))
        else:
            await ctx.send(sender, ClaimDetailsMessage(details=["No document text provided"]))

    def extract_details(self, document_text):
        preprocessed_text = document_text.strip()
        result = nlp_ner(preprocessed_text)
        details = [entity['word'] for entity in result]
        return details

# Initialize and run Agent2
agent2 = Agent2(name="agent2", seed="agent2 recovery phrase")

if __name__ == "__main__":
    agent2.run(port=8002)
