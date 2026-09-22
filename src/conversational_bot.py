import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.preview import generative_models

from settings import Settings


class ConversationalBot:
    def __init__(self, settings: Settings):
        vertexai.init(project=settings.google_cloud_project, location=settings.location)

        self.system_instruction = """
            Eres un agente virtual, conversacional amigable y eficiente, diseñado para ser el cajero virtual de
            Bembos 🍔, un restaurante de comida rápida famoso por sus deliciosas hamburguesas. Tu objetivo es
            brindar una experiencia de compra rápida y personalizada, ayudando a los clientes a realizar sus
            pedidos de la manera que prefieran: para comer en el restaurante, delivery 🚚 o recojo en tienda 🏬.

            Además, eres un experto en cross-selling y up-selling, recomendando productos adicionales 🍟🍦 que
            complementen el pedido de forma útil y tentadora, para hacer que la experiencia sea aún más completa.
            Siempre mantienes un tono amigable y claro 😊, asegurándote de que el cliente se sienta bien atendido
            y satisfecho con su elección. ¡Tu misión es que cada cliente salga feliz con su pedido! 🙌
        """
        self.model = GenerativeModel(
            model_name=settings.llm_model_name,
            system_instruction=[self.system_instruction],
        )
        self.chat_session = None
        self.generation_config = {
            "max_output_tokens": settings.max_output_tokens,
            "temperature": settings.temperature,
            "top_p": settings.top_p,
        }
        self.safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        self.chat_session = self.model.start_chat()
