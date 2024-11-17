import cv2
import zlib
import socket
import numpy as np

# Receiver settings
UDP_IP = "192.168.0.101"
UDP_PORT = 5005

# Receiver function
def receive_video():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print("Created and bound socket")

    frame_data = b'' 

    while True:
        data, addr = sock.recvfrom(65507)  # Adjust buffer size if necessary
        # print(f"Received data of size: {len(data)} bytes")

        frame_data += data

        if b'\xFF\xD9' in frame_data:  
            # print("JPEG marker is present")
            try:
                frame_data, remaining_data = frame_data.split(b'\xFF\xD9', 1)
                decompressed_data = zlib.decompress(frame_data)
                # print("decompressed image")

                frame = cv2.imdecode(np.frombuffer(decompressed_data, dtype=np.uint8), 1)
                cv2.imshow('Received', frame)
                cv2.waitKey(1)
            except zlib.error as e:
                print(f"Error decompressing frame: {e}")
            
            frame_data = remaining_data
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    sock.close()

# Start receiver
receive_video()
