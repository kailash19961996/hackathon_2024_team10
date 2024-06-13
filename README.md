# Automated Insurance Claim Processing Using GPT-4

## Description
This project leverages the power of the GPT-4 API to automate the processing of insurance claims. It consists of three agents that interact with documents containing insurance terms and conditions, user claims, and relevant rules. The agents collaborate to match user claims to the appropriate rules and determine the claim status.

- **Agent 1**: Extracts rules from the insurance terms and conditions document.
- **Agent 2**: Processes user claims by matching the information to certain fields.
- **Agent 3**: Receives information from Agent 1 and Agent 2, finds the relevant rule for the user claim, and determines the claim status.

## Instructions to Run the Project

### Setup Environment

- Ensure you have Python installed on your machine.
- Install necessary dependencies by running:

  ```bash
  pip install openai
