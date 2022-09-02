import pyautogui

import numpy as np
import cv2
from pyzbar import pyzbar


screenWidth, screenHeight= pyautogui.size()
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)
THICKNESS = 2
FONT = cv2.FONT_HERSHEY_DUPLEX
FONT_SCALE = 1
TEXT_THICKNESS = 1
 

def readBarcode(frame):
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:

        points = barcode.polygon
        x, y, w, h = barcode.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, RED, THICKNESS)

        barcodeData = barcode.data.decode('utf-8')
        barcodeType = barcode.type
        
        cv2.putText(frame, barcodeData, (x, y), FONT, FONT_SCALE, RED, TEXT_THICKNESS)
        
        with open(f"lastRecognizedBarcode.txt", mode ='w') as file:
            file.write(f"LAST RECOGNIZED BARCODE INFORMATION \n \
                Data: {barcodeData} \n \
                Type: {barcodeType}")
    return frame


def main():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, screenWidth)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, screenHeight)
    ret, frame = camera.read()

    while ret:
        ret, frame = camera.read()
        frame = readBarcode(frame)
        cv2.imshow('Barcode code scanner', frame)
        keyCode = cv2.waitKey(1)
        if keyCode & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty('Barcode code scanner', cv2.WND_PROP_VISIBLE) <1:
            break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()