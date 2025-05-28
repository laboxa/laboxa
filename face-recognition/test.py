import cv2

deviceid = 0  # カメラデバイスID
capture = cv2.VideoCapture(deviceid)

if not capture.isOpened():
    print("カメラのオープンに失敗しました")
    exit()

ret, frame = capture.read()
if not ret:
    print("フレームの取得に失敗しました")
    exit()

cv2.imwrite('test.jpg', frame)
capture.release()
cv2.destroyAllWindows()