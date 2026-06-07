# SimplifyGPT

SimplifyGPT breaks complex concepts into short, visual, step-by-step explanations.

The app takes a concept from the user, asks an OpenAI model to produce a structured explanation, generates image prompts for each step, creates images, and saves the final result as an explainer document.

## Features

- Streamlit UI for entering a concept and viewing the explanation
- Command-line entry point for quick local runs
- YAML-based response parsing for structured outputs
- DALL-E image generation for each explanation step
- Word document generation with text and images
- Timestamped output folders for generated artifacts
- Debug and error logging

## Project Structure

| Path | Purpose |
| --- | --- |
| `src/app.py` | Streamlit app entry point |
| `src/main.py` | Command-line entry point |
| `src/utils/` | OpenAI calls, YAML parsing, image generation, document creation, logging |
| `src/rendition/` | Streamlit rendering helpers |
| `config/initial_config.yaml` | Model, prompt, and image-generation settings |
| `prompts/` | Prompt templates used by the app |
| `images/` | Generated images |
| `output/` | Generated documents and run outputs |

## Quick Start

Clone the repo:

```bash
git clone https://github.com/FarzamHejaziK/SimplifyGPT.git
cd SimplifyGPT
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-openai-key"
```

Run the Streamlit app:

```bash
streamlit run src/app.py
```

Or run the command-line version:

```bash
python src/main.py
```

## Configuration

Main settings live in `config/initial_config.yaml`:

```yaml
openai:
  model: "chatgpt-4o-latest"
  api_key: ${OPENAI_API_KEY}
  system_prompt_path: "prompts/simplify_user_intent.txt"

chat:
  temperature: 0
  max_tokens: 4000

image_generation:
  size: "1024x1024"
  quality: "standard"
```

Change these values if you want to use a different model, prompt file, image size, or generation quality.

## How It Works

1. The user enters a concept.
2. The app loads the configured system prompt.
3. OpenAI returns a YAML-formatted explanation with steps and image descriptions.
4. The YAML parser converts the response into structured data.
5. The image helper generates one image per step.
6. The document helper writes a `.docx` explainer into `output/`.

## Notes

Generated files are written locally under `images/`, `output/`, and `logs/`. Keep your API key in the environment rather than committing it to the repository.
