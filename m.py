import google.generativeai as genai

# Configure API key
genai.configure(api_key="AIzaSyCS3BW1hhPOSX6OmGqYu-tIMKj7UniLMZw" )

# List available models
models = genai.list_models()
for model in models:
    print(model.name)