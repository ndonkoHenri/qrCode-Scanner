import cv2
import numpy as np
from datetime import datetime
from pyzbar.pyzbar import decode  # Pyzbar is useful for QRcodes decoding, and only it's "decode" method is needed
__start = datetime.now()    # Start time, for speed measurement
image_path = "test_images/qrcode2.jpg"  # Path to your Image
image = cv2.imread(image_path)
text_color = (255, 55, 50)  # Color of text found in the qrCode
bounding_box_color = (255, 55, 0)  # Text of rectangle surrounding qrCode


def qr_info_extractor(individual_qrcode):
    """Extracts all infos from the qr code by collecting them separately"""

    type = individual_qrcode.type
    data_in_bytes = individual_qrcode.data  # Data is normally in bytes ex: b'hello'
    data_in_string = data_in_bytes.decode("utf-8")  # we convert to string utf-8 for easy text display
    polygon = individual_qrcode.polygon
    rect = individual_qrcode.rect
    return type, data_in_string, polygon, rect  # infos needed about the qrCode


all_qrCodes = decode(image)  # Get all qrCodes in image by decoding

count = 1
for qrCode in all_qrCodes:
    """Take each individually and Get it's infos using the Extractor function"""

    qr_info_type, qr_info_data, qr_info_polygon, qr_info_rect, = qr_info_extractor(qrCode)
    points = np.array([qr_info_polygon], np.int32)  # shape = (1,4,2)
    points = points.reshape((-1, 1, 2))  # Reshaping must be done for the polyLines function

    cv2.polylines(image, [points], True, bounding_box_color, 2)  # Encloses the Qrcode on frame in a rectangle and shows

    # Get the Origin from the polygon informations
    qr_origin = (qr_info_polygon[0].x, qr_info_polygon[0].y)
    # Get the diagonal points to the origin for rectangle drawing, but not really useful in code
    qr_origin_diagonal = (qr_info_polygon[2].x, qr_info_polygon[2].y)
    cv2.putText(image, qr_info_data, (qr_info_rect[0], qr_info_rect[1] - 5), cv2.FONT_HERSHEY_COMPLEX, 0.35,
                text_color, 1)
    print(f"{count}-->", qr_info_data)
    count += 1
    cv2.imshow("qrCodeScanner - ndonkoHenri", image)
__end = datetime.now()
duration = __end - __start
print(duration)
cv2.waitKey(0)  # A delay function to see what happened
