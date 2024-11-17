import cv2
import zlib
import socket

UDP_IP = "192.168.0.100"  # reciver IP
UDP_PORT = 5005
cap = cv2.VideoCapture(0)
print('created camera')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('created socket')

def send_video():
    try:
        while True:
            ret, frame = cap.read()
            # print("read a new frame")
            if not ret:
                break
            
            _, buffer = cv2.imencode('.jpg', frame)
            compressed_data = zlib.compress(buffer, 2) + b'\xFF\xD9'
            
            chunk_size = 65507
            for i in range(0, len(compressed_data), chunk_size):
                chunk = compressed_data[i:i+chunk_size]
                sock.sendto(chunk, (UDP_IP, UDP_PORT))

    except Exception as e:
        print(e.with_traceback())
    
send_video()
cap.release()
sock.close()
print("released camera and closed socket")