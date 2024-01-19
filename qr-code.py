import os
import cv2
import qrcode
from pathlib import Path
from datetime import datetime

def qrcode_read():
    choice = input("Ler QR code:\nC - câmera\nD - diretório\nEscolha: ")

    if choice.upper() == "C":
        camera_id = 0
        delay = 1
        window_name = 'QR Code'

        qrcd = cv2.QRCodeDetector()
        cap = cv2.VideoCapture(camera_id)

        while True:
            ret, frame = cap.read()
            if ret:
                ret_qrcd, decoded_info, points, _ = qrcd.detectAndDecodeMulti(frame)
                if ret_qrcd:
                    for s, p in zip(decoded_info, points):
                        if s:
                            print("QRCODE", s)
                            color = (0, 255, 0)
                            frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)

                    cv2.imshow(window_name, frame)
                    cv2.waitKey(2000)
                    break

                cv2.imshow(window_name, frame)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        cap.release()

    elif choice.upper() == "D":
        # Escolher o arquivo de imagem
        file_path = input("Caminho completo do arquivo de imagem: ")
        
        if os.path.exists(file_path):
            frame = cv2.imread(file_path)
            qrcd = cv2.QRCodeDetector()
            ret_qrcd, decoded_info, points, _ = qrcd.detectAndDecodeMulti(frame)

            if ret_qrcd:
                for s, p in zip(decoded_info, points):
                    if s:
                        print("QRCODE", s)
                        color = (0, 255, 0)
                        frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)

                cv2.imshow("QR Code", frame)
                cv2.waitKey(2000)
            else:
                print("Nenhum QR code detectado na imagem.")
            
            cv2.destroyAllWindows()
        else:
            print("Caminho do arquivo inválido.")


def qrcode_create():
    text = input("Texto para gerar o QR code: ")

    # Criar o QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Criar a imagem do QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Encontrar o diretório "Downloads" no sistema
    download_dir = Path.home() / "Downloads"

    # Salvar o arquivo com timestamp na pasta "Downloads"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{download_dir}/qrcode_{timestamp}.png"
    img.save(filename)
    print(f"QR code gerado e salvo em: {filename}")

# Execução principal do programa
if __name__ == "__main__":
    while True:
        choice = input("L - ler qrcode\nG - gerar qrcode\nENTER - encerrar programa\nEscolha: ")

        if choice.upper() == "L":
            qrcode_read()
        elif choice.upper() == "G":
            qrcode_create()
        else:
            print("----------")
            break
