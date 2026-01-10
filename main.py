from infrastructure.ai.ocr_service_impl import LMStudioModel

if __name__ == "__main__":
    vl_model = LMStudioModel()
    image_path = "receipt_images/img_8.jpg"

    receipt = vl_model.process_receipt(image_path)
    print(*receipt['items'], sep='\n')
