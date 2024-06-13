# hackathon_2024_team10
hackathon_2024_team10
# PRT Pension schemes recommender

## hackathon_2024_team10

### Setup

```bash
python3 -m venv venv
source ./venv/bin/activate
source .env
pip install poetry 
poetry install
```

### Setup Open API / Groq Keys to access ChatGPT

##### Open AI API

https://www.datacamp.com/tutorial/guide-to-openai-api-on-tutorial-best-practices

Once the API keys are obtained, add them to the `.env` file as - 
```
OPEN_API_KEY=<YOUR OPEN API KEY HERE>
```

##### Groq  API
Open API might hit the quoata quickly. Use Groq with Mistral models instead.

https://console.groq.com/docs/quickstart

Once the API keys are obtained, add them to the `.env` file as - 
```
GROQ_API_KEY=<YOUR OPEN API KEY HERE>
```


### Background

This program recommends Pension schemes for employees based on the rquirements, reading an input CSV, using item-item filtering and retrieval augmented generation to get the desired outpute