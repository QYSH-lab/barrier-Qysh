import cv2 as cv
import imutils
import numpy as np
import pytesseract
import requests

# === Настройки ===
SERVER_URL = "http://172.20.10.4:5000/plate"  # ПК1
IMAGE_PATH = "car3.jpeg"  # тестовая фотка

# Путь к Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv.imread(IMAGE_PATH)
if img is None:
    raise FileNotFoundError(f"Не удалось открыть {IMAGE_PATH}")

img = imutils.resize(img, width=620)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.bilateralFilter(gray, 13, 15, 15)
edged = cv.Canny(gray, 30, 200)

cnts = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:10]
screenCnt = None

for c in cnts:
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.018 * peri, True)
    if len(approx) == 4:
        screenCnt = approx
        break

plate_text = ""

if screenCnt is not None:
    mask = np.zeros(gray.shape, np.uint8)
    cv.drawContours(mask, [screenCnt], 0, 255, -1)
    x, y, w, h = cv.boundingRect(screenCnt)
    plate = img[y:y+h, x:x+w]

    plate_gray = cv.cvtColor(plate, cv.COLOR_BGR2GRAY)
    plate_gray = cv.GaussianBlur(plate_gray, (3,3), 0)
    plate_gray = cv.adaptiveThreshold(plate_gray, 255,
                                      cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv.THRESH_BINARY, 11, 2)
    plate_gray = cv.resize(plate_gray, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)

    config = "--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    text = pytesseract.image_to_string(plate_gray, config=config).strip()
    plate_text = text.replace(" ", "").upper()

    print(f"[VISION] Распознан номер: {plate_text}")

if plate_text:
    try:
        resp = requests.post(SERVER_URL, json={'plate': plate_text})
        print("[VISION] Ответ сервера:", resp.json())
    except Exception as e:
        print("[VISION] ❌ Ошибка отправки:", e)
else:
    print("[VISION] ❌ Номер не распознан")