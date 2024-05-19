import cv2
import pyzbar.pyzbar as pyzbar
import time  # 시간 지연을 위한 모듈

font = cv2.FONT_HERSHEY_SIMPLEX

# QR코드 인식 및 테두리 설정
def read_frame(frame):
    try:
        # QR코드 정보 decoding
        barcodes = pyzbar.decode(frame)
        # QR코드 정보가 여러개 이기 때문에 하나씩 해석
        barcode_data = []
        for barcode in barcodes:
            # QR코드 rect정보
            x, y, w, h = barcode.rect
            # QR코드 데이터 디코딩
            barcode_info = barcode.data.decode('utf-8')
            barcode_data.append(barcode_info)
            # 인식한 QR코드 사각형 표시
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # 인식한 QR코드 사각형 위에 글자 삽입
            cv2.putText(frame, barcode_info, (x , y - 20), font, 0.5, (0, 0, 255), 1)

        return frame, barcode_data
    except Exception as e:
        print(e)
        return frame, []

def detect_qr_code_from_camera(timeout=5):
    try:
        # 웹캠 불러오기
        cap = cv2.VideoCapture(0)
        qr_code_detected = False
        detection_time = None
        detected_data = []

        # 웹캠 연결 확인 및 영상 재생
        while cap.isOpened():
            # 프레임 가져오기
            ret, frame = cap.read() #재생되는 영상을 한 프레임씩 제대로 읽었다면 ret 값이
            #True가 되고, 실패하면 False가 된다. 읽은 프레임은 frame에 저장된다.
            # 프레임이 존재하면
            if ret: #프레임씩 제대로 읽고 있다면 아래 코드 동작
                # QR코드 인식
                frame, barcode_data = read_frame(frame)
                # 프레임 출력
                cv2.imshow("barcode reader", frame)
                
                if barcode_data and not qr_code_detected:
                    qr_code_detected = True
                    detection_time = time.time()  # QR 코드가 인식된 시간 기록
                    detected_data = barcode_data
                
                # QR 코드가 인식된 후 timeout 초가 지나면 종료
                if qr_code_detected and (time.time() - detection_time > timeout):
                    break
                
                if cv2.waitKey(1) == 27:  # ESC 키를 누르면 종료
                    break
            else:
                print("예외")
                break

    except Exception as e:
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    return detected_data

if __name__ == '__main__':
    data = detect_qr_code_from_camera()
    print(data)
