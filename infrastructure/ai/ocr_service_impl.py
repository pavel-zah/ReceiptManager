from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from application.interfaces.ocr_service import OCRService
from application.dto.receipt_dto import ParsedReceiptDTO
from langchain_core.messages import HumanMessage
import lmstudio as lms



MODEL_NAME = "qwen/qwen3-vl-4b"

SYSTEM_PROMPT = """
                 Ты - полезный агент, специалист по распознаванию чеков.
                 Твоя работа заключается в извлечении из фотографии чека всех позиций в заказе с указанием их цены.
                 Если ты не можешь разобрать позиции с фото чека, то ты ничего не придумываешь, а говоришь это прямо.
                 Если при распознавании чека произошла ошибка, то записывай ее в поле error,
                 если ошибок не было то оставляешь поле пустым.
                 """

class QwenVL(OCRService):

    def __init__(self):

        model = ChatOpenAI(
            model=MODEL_NAME,
            openai_api_base="http://localhost:1234/v1",
            openai_api_key="not-needed",
            temperature=0.3,
            timeout=10,
        )

        self.agent = create_agent(
            model=model,
            system_prompt=SYSTEM_PROMPT,
            # response_format=ToolStrategy(ParsedReceiptDTO),
        )

    def process_receipt(self, image_path: str) -> ParsedReceiptDTO:
        # возможно надо так же передавать расширение файла
        image_handle = lms.prepare_image(image_path)
        image_message = image_handle.to_dict()

        message = HumanMessage(
            content= [
                image_message
            ]
        )

        # message = {
        #     "role": "user",
        #     "content": [
        #       {
        #         "type": "text",
        #         "text": "распиши все позиции из чека с ценой"
        #       },
        #       {
        #         "type": "file",
        #         "name": "img_8.jpg",
        #         "identifier": r"C:\Users\pzaha\PycharmProjects\ReceiptManager\receipt_images\img_8.jpg",
        #         "sizeBytes": 434033,
        #         "fileType": "image"
        #       }
        #     ]
        #   }

        response = self.agent.invoke(message)
        return response
        # return response['structured_response']


class LMStudioModel(OCRService):

    def __init__(self):

        self.model = lms.llm(
            MODEL_NAME
        )


    def process_receipt(self, image_path: str) -> ParsedReceiptDTO:
        # возможно надо так же передавать расширение файла
        image_handle = lms.prepare_image(image_path)
        print(image_handle.to_dict())
        chat = lms.Chat()
        chat.add_user_message("Распознай все позиции из этого чека с их ценами", images=[image_handle])
        print(chat)
        # prediction = self.model.respond(chat)

        return None
        # return response['structured_response']
