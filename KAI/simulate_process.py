# simulate_process.py
from uagents import Context
from message_models import DocumentAMessage, DocumentCMessage

# Assuming agents are running on localhost and their respective ports
agent1_address = "http://localhost:8001"
agent2_address = "http://localhost:8002"

# Simulate sending documents to the agents
document_a_text = extract_text_from_pdf("path/to/documentA.pdf")
document_c_text = extract_text_from_pdf("path/to/documentC.pdf")

# Send messages to agents
context = Context()
await context.send(agent1_address, DocumentAMessage(text=document_a_text))
await context.send(agent2_address, DocumentCMessage(text=document_c_text))
