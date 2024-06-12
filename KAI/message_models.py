# message_models.py
from uagents import Model

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
