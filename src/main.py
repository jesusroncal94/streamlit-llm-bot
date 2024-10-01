import streamlit

from conversational_bot import ConversationalBot
from settings import Settings

if __name__ == "__main__":
    settings = Settings()
    bot = ConversationalBot(settings=settings)
    streamlit.title("Pide tu Bembos!")

    if "chat" not in streamlit.session_state:
        streamlit.session_state["chat"] = bot.chat_session

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
