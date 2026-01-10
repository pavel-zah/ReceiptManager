from application.interfaces.ocr_service import OCRService
from application.dto.receipt_dto import ParsedReceiptDTO
import lmstudio as lms


MODEL_NAME = "qwen/qwen3-vl-4b"

SYSTEM_PROMPT = """
                 Ты - полезный агент, специалист по распознаванию чеков.
                 Твоя работа заключается в извлечении из фотографии чека всех позиций в заказе с указанием их цены.
                 -Если при распознавании чека произошла ошибка,то ты ничего не придумываешь,
                  записывай ошибку ее в поле error, а позицию пропускай, сли ошибок не было то оставляешь поле пустым.
                 """

class LMStudioModel(OCRService):
    def __init__(self):

        self.model = lms.llm(
            MODEL_NAME
        )

    def process_receipt(self, image_path: str) -> ParsedReceiptDTO:
        image_handle = lms.prepare_image(image_path)
        chat = lms.Chat()
        chat.add_user_message("Распознай все позиции из этого чека с их ценами", images=[image_handle])
        prediction = self.model.respond(chat, response_format=ParsedReceiptDTO)
        return prediction.parsed


