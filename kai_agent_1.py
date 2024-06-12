from uagents import Agent, Bureau, Context, Model
import fitz  # PyMuPDF
from transformers import pipeline

# Initialize the Hugging Face NLP pipeline
# Note: Adjust the model according to your requirements. You can use a model from Hugging Face's model hub.
# For example, using a summarization model that can help in extracting key points.
nlp = pipeline("summarization", model="facebook/bart-large-cnn")

# Define the Message model
class DocumentMessage(Model):
    text: str

class ResponseMessage(Model):
    rules: list

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

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

        # Use the Hugging Face pipeline to summarize and extract key points from the document text
        result = nlp(preprocessed_text, max_length=512, min_length=30, do_sample=False)

        # Extract the summarized points as rules
        rules = [summary['summary_text'] for summary in result]

        return rules

# Create the Requesting Agent
class RequestingAgent(Agent):
    def __init__(self, name: str, seed: str):
        super().__init__(name=name, seed=seed)

    @Agent.on_interval(period=3.0)
    async def send_message(self, ctx: Context):
        # Extract text from the PDF document
        pdf_path = "path/to/your/document.pdf"  # Update with your PDF path
        document_text = extract_text_from_pdf(pdf_path)
        await ctx.send(parsing_agent.address, DocumentMessage(text=document_text))

    @Agent.on_message(model=ResponseMessage)
    async def handle_response(self, ctx: Context, sender: str, msg: ResponseMessage):
        ctx.logger.info(f"Received rules from {sender}: {msg.rules}")
        print(f"Received rules: {msg.rules}")

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
