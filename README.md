# barrier-Qysh
Для начала работы необходимо скачать библиотеки на каждый сервер

Открываем cmd и прописываем команды для каждого пк
flask-server: pip install pandas
pip install requests
arduino-connect: pip install pyserial
для client-cv необходимо скачать компьютерное зрение tesseract: https://github.com/UB-Mannheim/tesseract/wiki
после сделать путь для него: pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
и ввести команду в cmd: pip install opencv-python imutils numpy pytesseract requests
flask-server и arduino-connect обязательно открывается в cmd, client-cv можно открыть в vs code или pycharm.

Нужно не забывать что в коде нужно поменять пути ip компьтеров (в client-cv SERVER_URL = "http://XXX.XX.XX.X:500X/plate", в flask-server CLIENT_ARDUINO_URL = "http://XXX.XX.XX.X:500X/command")
Также в flask-server необходимо поменять путь для Excel файла с базой данных номерных знаков(EXCEL_FILE = r"C:\Users\User\Desktop\schlagbaum\spisoknomerov.xlsx")
Не забывайте что arduino нужно подключить к нужному порту в arduino-connect(arduino = serial.Serial('COM3', 9600, timeout=1))
В servo.ino код от arduino, используйте car3.jpeg или камеру для считывания номеров(так же не забудте поменять путь IMAGE_PATH = "car3.jpeg" либо добавить камеру VIDEO_SOURCE = 0)

Когда все библиотеки были скачаны можно работать над чтением номеров для шлагбаума. flask-server и arduino-connect имеют свои "сервера" которые взаимодействуют дру гс другом и посылают команды. client-cv считывает номер и отправляет результат в flask-server, flask-server считывает информацию и сверяет с базой данных(excel file) на наличие номера, если номер есть в базе, flask-server отправляет команду (True) arduino-connect и заставляя сервопривод двигаться. Если номера нету в базе данных отправляется команда (False) и client-cv бездействует
