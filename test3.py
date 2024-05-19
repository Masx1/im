import cv2
import pyzbar.pyzbar as pyzbar

font = cv2.FONT_HERSHEY_SIMPLEX #영상에 표시할 폰트

# QR코드 인식 및 테두리 설정
def read_frame(frame):
    try:
        # QR코드 정보 decoding
        barcodes = pyzbar.decode(frame)
        # Pyzbar를 사용하여 프레임 내의 QR 코드를 디코딩한다.
        # 여러 개의 QR 코드가 있을 수 있으므로 리스트로 반환된다.
        
        # QR코드 정보가 여러개 이기 때문에 하나씩 해석
        for barcode in barcodes:
            # QR코드 rect정보
            x, y, w, h = barcode.rect # QR 코드의 위치와 크기를 가져온다
            # QR코드 데이터 디코딩
            barcode_info = barcode.data.decode('utf-8')
            # 인식한 QR코드 사각형 표시
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # 인식한 QR코드 사각형 위에 글자 삽입
            cv2.putText(frame, barcode_info, (x , y - 20), font, 0.5, (0, 0, 255), 1)

        return frame
    except Exception as e:
        print(e)


def main():
    try:
        # 웹캠 불러오기 /0번 카메라 영상 객체 가져오기
        cap = cv2.VideoCapture(0)

        # 웹캠 연결 확인 및 영상 재생
        while cap.isOpened(): # 영상 파일(카메라)이 정상적으로 열렸는지(초기화되었는지) 여부
            # 프레임 가져오기
            ret, frame = cap.read() #재생되는 영상을 한 프레임씩 제대로 읽었다면 ret 값이
            #True가 되고, 실패하면 False가 된다. 읽은 프레임은 frame에 저장된다.
            # 프레임이 존재하면
            if ret: #프레임씩 제대로 읽고 있다면 아래 코드 동작
                # QR코드 인식
                frame = read_frame(frame)
                # 프레임 출력
                cv2.imshow("barcode reader", frame) #프레임을 윈도우에 표시
                if cv2.waitKey(1) == 27: #  1밀리초 동안 키 입력을 기다리고, ESC 키(ASCII 27)가 눌리면 반복을 종료.
                    break
            else:
                print("예외")
                break

    except Exception as e:
        print(e)
    finally:
        cap.release() # 영상 파일(카메라) 사용을 종료
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
