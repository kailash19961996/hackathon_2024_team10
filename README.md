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

###  2. Prepare Documents
- Place the documentA_insurance_terms.docx and documentB_claim_details.docx files in the data directory.
- Ensure the documentA_rules.txt and documentB_claims.txt files are also in the data directory.


### 3. Run Agents
### Start Agent 1 to extract rules

- python agent1chatGPT.py
<img width="1438" alt="Screenshot 2024-06-13 at 11 48 48 AM" src="https://github.com/kailash19961996/hackathon_2024_team10/assets/123597753/da01fc79-1300-4272-974a-5d2f13b9500a">


### Start Agent 2 to process user claims

- python agent2chatGPT.py
<img width="1438" alt="Screenshot 2024-06-13 at 11 49 19 AM" src="https://github.com/kailash19961996/hackathon_2024_team10/assets/123597753/5390e42d-ef39-47f7-85e2-2a27571f3883">

### Start Agent 3 to match claims to rules

- python agent3chatGPT.py
<img width="743" alt="Screenshot 2024-06-13 at 11 58 53 AM" src="https://github.com/kailash19961996/hackathon_2024_team10/assets/123597753/3032a7e4-3494-4b85-9e62-ff96ab18dfc1">

<img width="743" alt="Screenshot 2024-06-13 at 11 59 06 AM" src="https://github.com/kailash19961996/hackathon_2024_team10/assets/123597753/a235eeba-3b57-47d1-9a46-7bf8b62dd487">



## Use-case Example

### Scenario

- John Doe, a user with ID 12345, requests early retirement due to ill health at the age of 58.
- Jane Smith, a user with ID 67890, requests normal retirement at the age of 65.

## Process

#### Agent 1 extracts the following relevant rule for early retirement due to ill health from documentA_insurance_terms.docx:
-  Rule 2.2.2 Early Retirement Ill Health Eligibility:
-  Members can retire at any age if the Scheme’s “Incapacity” definition is met.
-  Price Range: $200-$1000 per assessment

#### Agent 2 processes the claim details from documentB_claim_details.docx:
-  John Doe: early retirement, age: 58, ill_health: yes, current_pension: $2500
-  Jane Smith: normal retirement, age: 65, ill_health: no, current_pension: $3000

#### Agent 3 matches John Doe's claim to the rule extracted by Agent 1 and determines the claim status:
-  Claim Status: Approved
-  Relevant Rule: Early Retirement Ill Health Eligibility

## Special Considerations
- Ensure the documents are formatted correctly for accurate processing.
- Review the extracted rules and matched results for accuracy before making final decisions.
- Maintain the confidentiality and security of user data throughout the process.

## Some Code Snippets

### Agent 1: Extracting Rules

  ```bash
  import openai
  def extract_rules(file_path):
      # Load and process the document
      with open(file_path, 'r') as file:
          content = file.read()
      # Extract rules using GPT-4
      response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[{"role": "system", "content": "Extract rules from the document."},
                    {"role": "user", "content": content}]
      )
      rules = response['choices'][0]['message']['content']
      return rules
  if __name__ == "__main__":
      rules = extract_rules('data/documentA_rules.txt')
      print(rules)

### Agent 2: Processing Claims

  ```bash
  import openai  
  def process_claims(file_path):
      # Load and process the document
      with open(file_path, 'r') as file:
          content = file.read()
      # Extract claims using GPT-4
      response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[{"role": "system", "content": "Process user claims from the document."},
                    {"role": "user", "content": content}]
      )
      claims = response['choices'][0]['message']['content']
      return claims
  if __name__ == "__main__":
      claims = process_claims('data/documentB_claims.txt')
      print(claims)

### Agent 3: Matching Claims to Rules

  ```bash
  import openai
  def match_claims_to_rules(claims, rules):
      # Match claims to rules using GPT-4
      response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[{"role": "system", "content": "Match claims to rules."},
                    {"role": "user", "content": f"Claims: {claims}\nRules: {rules}"}]
      )
      matched_results = response['choices'][0]['message']['content']
      return matched_results
  if __name__ == "__main__":
      claims = ... # Load claims from Agent 2
      rules = ... # Load rules from Agent 1
      results = match_claims_to_rules(claims, rules)
      print(results)







