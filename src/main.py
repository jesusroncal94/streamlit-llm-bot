import streamlit

from conversational_bot import ConversationalBot
from settings import Settings


@streamlit.cache_resource
def load_bot() -> ConversationalBot:
    return ConversationalBot(settings=Settings())


if __name__ == "__main__":
    bot = load_bot()
    streamlit.title("Pide tu Bembos!")

    if "chat" not in streamlit.session_state:
        streamlit.session_state["chat"] = bot.start_chat()

    if "messages" not in streamlit.session_state:
        streamlit.session_state["messages"] = []

    for message in streamlit.session_state["messages"]:
        with streamlit.chat_message(message["role"]):
            streamlit.markdown(message["content"])

    if prompt := streamlit.chat_input("Describe tu antojo de hoy!"):
        streamlit.session_state["messages"].append({"role": "user", "content": prompt})
        with streamlit.chat_message("user"):
            streamlit.markdown(prompt)

        with streamlit.chat_message("assistant"):
            response = streamlit.session_state["chat"].send_message(
                content=prompt,
                generation_config=bot.generation_config,
                safety_settings=bot.safety_settings,
            )
            streamlit.markdown(response.text)

        streamlit.session_state["messages"].append(
            {"role": "assistant", "content": response.text}
        )
