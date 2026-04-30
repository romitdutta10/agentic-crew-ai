# Lite LLM

Step 1 : Pull Docker image

docker pull ghcr.io/berriai/litellm-database:main-latest

Step 2 : Set up database

    2.1 GEt Docker componse and setup .env

    # Get the docker compose file
curl -O https://raw.githubusercontent.com/BerriAI/litellm/main/docker-compose.yml

# Add the master key - you can change this after setup
echo 'LITELLM_MASTER_KEY="sk-1234"' > .env

# Add the litellm salt key — cannot be changed after adding a model
# Used to encrypt/decrypt your LLM API key credentials
# Generate a strong random value: https://1password.com/password-generator/
echo 'LITELLM_SALT_KEY="sk-1234"' >> .env

# Add your model credentials
echo 'AZURE_API_BASE="https://openai-***********/"' >> .env
echo 'AZURE_API_KEY="your-azure-api-key"' >> .env

2.2 — Create config.yaml

model_list:
  - model_name: gpt-4o
    litellm_params:
      model: azure/my_azure_deployment
      api_base: os.environ/AZURE_API_BASE
      api_key: os.environ/AZURE_API_KEY
      api_version: "2025-01-01-preview"

general_settings:
  master_key: sk-1234 # 🔑 your proxy admin key (must start with sk-)
  database_url: "postgresql://llmproxy:dbpassword9090@db:5432/litellm"

2.3 — Create prometheus.yml

global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "litellm"
    static_configs:
      - targets: ["litellm:4000"]