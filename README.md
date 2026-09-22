# streamlit-llm-bot

A conversational ordering assistant built with Streamlit and Google Vertex AI. It plays the counter staff of a fast-food restaurant: it takes an order in natural language, asks what it needs to ask, and suggests the sides and drinks that go with what you picked.

The chat loop is short. What makes the behaviour is the system instruction and the generation settings around it — which is the part worth reading.

## What it does

The model is given a persona and a job: greet the customer, work out whether the order is for the table, for delivery, or for pickup, and recommend complements without being pushy. Cross-selling and up-selling are stated goals in the prompt rather than post-processing rules, so the suggestions arrive inside the conversation instead of as a banner beside it.

Conversation state lives in Streamlit's session state, so the model receives the full history on every turn and the page survives reruns without losing the thread.

## Configuration

Settings are validated by Pydantic at startup, so an out-of-range temperature fails immediately rather than at the first request.

```
GOOGLE_CLOUD_PROJECT=your-gcp-project
LOCATION=us-central1
LLM_MODEL_NAME=gemini-1.5-flash
MAX_OUTPUT_TOKENS=1024
TEMPERATURE=0.7
TOP_P=0.95
```

| Variable | Constraint |
| --- | --- |
| `MAX_OUTPUT_TOKENS` | greater than 0 |
| `TEMPERATURE` | between 0.0 and 2.0 |
| `TOP_P` | between 0.0 and 1.0 |

Safety filters are set to block medium-and-above for hate speech, dangerous content, sexually explicit material, and harassment.

## Running it

Requires Python 3.10+, [uv](https://docs.astral.sh/uv/), and Google Cloud credentials with access to Vertex AI.

```bash
gcloud auth application-default login
uv run streamlit run src/main.py
```

The interface opens at <http://localhost:8501>.

## How the code is organised

```
src/
├── main.py               Streamlit page and the chat loop
├── conversational_bot.py The persona, the model, and its generation settings
└── settings.py           Validated configuration
```

`ConversationalBot` owns everything about the model and hands back a chat session. `main.py` only renders and forwards messages, so changing the persona, the model, or the safety thresholds never touches the interface.

## License

MIT — see [LICENSE](LICENSE).
