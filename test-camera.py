import cv2

class Camera:
    def __init__(self):
        self.source = 0  # Cambia a 1 si tienes más cámaras
        self.resolution = (320, 240)
        self.format = 'YUYV'

        self.capture = cv2.VideoCapture(self.source)
        if not self.capture.isOpened():
            raise ValueError("Error opening video source")
        
        # Establecer resolución
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        
        # Establecer formato de pixel
        fourcc = cv2.VideoWriter_fourcc(*self.format)
        self.capture.set(cv2.CAP_PROP_FOURCC, fourcc)

        # Imprimir información de la cámara
        self.print_camera_info()

    def print_camera_info(self):
        width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"Resolución configurada: {width}x{height}")

    def get_frame(self):
        for attempt in range(5):  # Intenta capturar hasta 5 veces
            ret, frame = self.capture.read()
            if ret:
                print("Frame capturado exitosamente.")
                return frame
            else:
                print(f"No se pudo capturar un frame en el intento {attempt + 1}. Retorno: {ret}")
                # Imprime el estado de la cámara
                print("Estado de la cámara:")
                print(f"  CAP_PROP_FRAME_WIDTH: {self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)}")
                print(f"  CAP_PROP_FRAME_HEIGHT: {self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
                print(f"  CAP_PROP_FOURCC: {self.capture.get(cv2.CAP_PROP_FOURCC)}")
                print(f"  CAP_PROP_FPS: {self.capture.get(cv2.CAP_PROP_FPS)}")
                print(f"  CAP_PROP_POS_FRAMES: {self.capture.get(cv2.CAP_PROP_POS_FRAMES)}")
        
        return None

    def release(self):
        self.capture.release()

if __name__ == "__main__":
    cam = Camera()
    frame = cam.get_frame()

    if frame is not None:
        cv2.imwrite("captured_image.jpg", frame)
        print("Imagen capturada y guardada como 'captured_image.jpg'.")
    else:
        print("No se pudo capturar la imagen.")

    cam.release()
