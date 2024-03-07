import cv2
import os
import time

def capture_image(resolution, num_photos, time_delay):
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Set the resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # Ruta completa al directorio del escritorio
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'images')

    # Create a folder to save the images
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    # Capture the specified number of photos
    for i in range(num_photos):
        # Capture a frame
        ret, frame = cap.read()

        # Guardar el frame como una imagen
        image_path = os.path.join(desktop_path, f'image_{i}.jpg')
        cv2.imwrite(image_path, frame)

        # Mostrar el frame
        cv2.imshow('Frame', frame)

        # Esperar el tiempo especificado
        time.sleep(time_delay)

        # Romper el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

def main():
    # Obtener la resolución, número de fotos y tiempo de espera del usuario
    resolution = (1080, 720)
    num_photos = int(input("Ingresa el número de fotos que deseas tomar: "))
    time_delay = float(input("Ingresa el tiempo de espera en segundos entre fotos: "))

    # Capturar las imágenes
    capture_image(resolution, num_photos, time_delay)

if __name__ == "__main__":
    main()
