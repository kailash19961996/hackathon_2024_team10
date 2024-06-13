# Automated Insurance Claim Processing Using GPT-4

## Description
This project leverages the power of the GPT-4 API to automate the processing of insurance claims. It consists of three agents that interact with documents containing insurance terms and conditions, user claims, and relevant rules. The agents collaborate to match user claims to the appropriate rules and determine the claim status.

- **Agent 1**: Extracts rules from the insurance terms and conditions document.
- **Agent 2**: Processes user claims by matching the information to certain fields.
- **Agent 3**: Receives information from Agent 1 and Agent 2, finds the relevant rule for the user claim, and determines the claim status.

## Instructions to Run the Project

### 1. Setup Environment

- Ensure you have Python installed on your machine.
- Install necessary dependencies by running:

  ```bash
  pip install openai

### 2. Prepare Documents
- Place the documentA_insurance_terms.docx and documentB_claim_details.docx files in the data directory.
- Ensure the documentA_rules.txt and documentB_claims.txt files are also in the data directory.

### 3. Run Agents
- Start Agent 1 to extract rules

  ```bash
  python agent1chatGPT.py

- Start Agent 2 to process user claims

  ```bash
  python agent2chatGPT.py

- Start Agent 3 to match claims to rules

  ```bash
  python agent3chatGPT.py

## Use-case Example

### Scenario

- John Doe, a user with ID 12345, requests early retirement due to ill health at the age of 58.
- Jane Smith, a user with ID 67890, requests normal retirement at the age of 65.

## Process

- Agent 1 extracts the following relevant rule for early retirement due to ill health from documentA_insurance_terms.docx:

-- Rule 2.2.2 Early Retirement Ill Health Eligibility:
-- Members can retire at any age if the Scheme’s “Incapacity” definition is met.
-- Price Range: $200-$1000 per assessment
