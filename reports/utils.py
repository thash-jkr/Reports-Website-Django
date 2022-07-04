import base64, uuid

from django.core.files.base import ContentFile

def GetReportImage(data):
    _, image_str = data.split(";base64")
    decoded_image = base64.b64decode(image_str)
    image_name = str(uuid.uuid4())[:10] + ".png"
    value = ContentFile(decoded_image, name=image_name)
    return value