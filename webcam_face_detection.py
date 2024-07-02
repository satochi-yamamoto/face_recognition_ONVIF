import cv2
import face_recognition
import time
import numpy as np
from onvif import ONVIFCamera
from datetime import datetime
import logging

# Configuração do logging para gravar no diretório C:\Scan_out
log_directory = r'C:\Scan_out'
log_file = log_directory + r'\face_recognition_app.log'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_file),
                        logging.StreamHandler()
                    ])
def is_image_blurry(image, threshold=100):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < threshold

# Conectar à câmera ONVIF com repetição de tentativas
def connect_to_onvif_camera(host, port, user, password, max_retries=5):
    for attempt in range(max_retries):
        try:
            logging.info(f"Tentativa {attempt + 1} de conectar à câmera ONVIF")
            camera = ONVIFCamera(host, port, user, password)
            logging.debug(f"ONVIFCamera inicializada: {camera}")
            media_service = camera.create_media_service()
            logging.debug(f"Serviço de mídia criado: {media_service}")
            profiles = media_service.GetProfiles()
            logging.debug(f"Perfis obtidos: {profiles}")
            token = profiles[0].token
            logging.debug(f"Token do perfil: {token}")
            stream_setup = {'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}, 'ProfileToken': token}
            uri = media_service.GetStreamUri(stream_setup)
            logging.info("Conexão estabelecida com sucesso")
            return uri.Uri
        except Exception as e:
            logging.error(f"Erro ao conectar à câmera ONVIF: {e}")
            if attempt < max_retries - 1:
                logging.info("Tentando novamente em 5 segundos...")
                time.sleep(5)
            else:
                logging.error("Máximo de tentativas atingido. Não foi possível conectar à câmera ONVIF.")
                raise

# Configurações da câmera IP ONVIF
host = '10.10.20.100'  # IP da câmera
port = 80
user = 'admin'
password = 'gap35ds3'

try:
    stream_uri = connect_to_onvif_camera(host, port, user, password)
    # Adicionando autenticação à URL do stream RTSP
    stream_uri_with_auth = f"rtsp://{user}:{password}@{host}:554/{stream_uri.split('://')[1]}"
    logging.info(f"URL do stream RTSP com autenticação: {stream_uri_with_auth}")
except Exception as e:
    logging.error(f"Não foi possível obter o URI do stream: {e}")
    exit(1)

# Configurar OpenCV para ler o stream de vídeo
cap = cv2.VideoCapture(stream_uri_with_auth)

if not cap.isOpened():
    logging.error("Não foi possível abrir o stream de vídeo")
    exit(1)

pessoa_identificada = False
face_count = 0
known_faces_encodings = []
face_id_mapping = {}

def log_face_recognition(face_id):
    with open(log_file, "a") as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now} - Face {face_id} reconhecida\n")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.warning("Não foi possível ler o frame do stream de vídeo")
            continue

        if frame is None or frame.size == 0:
            logging.warning("Frame vazio ou nulo recebido do stream de vídeo")
            continue

        if is_image_blurry(frame):
            if pessoa_identificada:
                print("Nenhuma pessoa identificada (imagem borrada)")
                pessoa_identificada = False
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_detected = False
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces_encodings, face_encoding, tolerance=0.6)
            if not any(matches):
                face_count += 1
                face_id = face_count
                known_faces_encodings.append(face_encoding)
                face_id_mapping[face_id] = face_encoding
                log_face_recognition(face_id)
            else:
                face_id = matches.index(True) + 1
                log_face_recognition(face_id)
            face_detected = True

        if face_detected:
            if not pessoa_identificada:
                print("Pessoa Identificada")
                pessoa_identificada = True
        else:
            if pessoa_identificada:
                print("Nenhuma pessoa identificada")
                pessoa_identificada = False

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    logging.error(f"Erro durante a execução: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
