import cv2
import numpy as np
from datetime import datetime  # For the saving of frames/images
from pyzbar.pyzbar import decode  # Pyzbar is useful for QRcodes decoding, and only it's "decode" method is needed

cap = cv2.VideoCapture(0)  # 0 for the computer's main-webcam. Try 1 or more for attached webcams
text_color = (255, 55, 50)  # Color of text found in the qrCode
bounding_box_color = (255, 55, 0)  # Text of rectangle surrounding qrCode


def empty(x):
    """Used by trackbars, so nothing is done when trackbar values get changed"""
    pass


cv2.namedWindow("Trackbars")  # A trackbar window is created
cv2.resizeWindow("Trackbars", 420, 55)  # Resize if necessary
cv2.createTrackbar("Brightness", "Trackbars", 70, 150, empty)  # A trackbar to adjust brightness settings


def qr_info_extractor(individual_qrcode):
    """Extracts all infos from the qr code by collecting them separately"""

    type = individual_qrcode.type
    data_in_bytes = individual_qrcode.data  # Data is normally in bytes ex: b'hello'
    data_in_string = data_in_bytes.decode("utf-8")  # we convert to string utf-8 for easy text display
    polygon = individual_qrcode.polygon
    rect = individual_qrcode.rect
    return type, data_in_string, polygon, rect  # infos needed about the qrCode


while True:
    sucess, image = cap.read()
    cap.set(10, cv2.getTrackbarPos("Brightness", "Trackbars"))  # Brightness adaptation from Trackbar

    all_qrCodes = decode(image)  # Get all qrCodes in image by decoding

    cv2.imshow("qrCodeScanner - ndonkoHenri", image)
    for qrCode in all_qrCodes:
        """Take each individually and Get it's infos using the Extractor function"""
        qr_info_type, qr_info_data, qr_info_polygon, qr_info_rect, = qr_info_extractor(qrCode)
        points = np.array([qr_info_polygon], np.int32)  # shape = (1,4,2)
        points = points.reshape((-1, 1, 2))  # Reshaping must be done for the polyLines function

        cv2.polylines(image, [points], True, bounding_box_color,
                      5)  # Encloses the Qrcode on frame in a rectangle and shows

        # Get the Origin from the polygon informations
        qr_origin = (qr_info_polygon[0].x, qr_info_polygon[0].y)
        # Get the diagonal points to the origin for rectangle drawing, but not really useful in code
        qr_origin_diagonal = (qr_info_polygon[2].x, qr_info_polygon[2].y)
        # The RECT value are used because they are fixed(Do not rotate when item or camera is turned) compared to polygon values
        cv2.putText(image, qr_info_data, (qr_info_rect[0], qr_info_rect[1] - 5), cv2.FONT_HERSHEY_COMPLEX, 0.35,
                    text_color, 1)
        # The image is shown after having detected  and shown all the barcodes
        cv2.imshow("qrCodeScanner - ndonkoHenri", image)
    # A delay function to see what happened
    image_shape = image.shape
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

"""     # Save a frame/actual image (Still in development)  # Help will be appreciated ! 
    elif cv2.waitKey(1) & 0xFF == ord('s'):
        print("s pressed")
        x = cv2.imwrite(f"{datetime.now}.jpg",image)
        if x:
            cv2.putText(image, "SAVED",(20,50),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),2)
            cv2.imshow("qrCodeScanner - ndonkoHenri", image)

            cv2.waitKey(500)
"""
