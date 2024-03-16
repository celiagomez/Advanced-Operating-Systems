import cv2
import os
import time
from datetime import datetime
from reportlab.pdfgen import canvas
from PIL import Image

def initialize_camera(resolution):
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Set the resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    return cap

def create_folder(folder_path):
    # Create a folder if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def save_image(image_path, frame, timestamp):
    # Save the frame as an image
    try:
        cv2.imwrite(image_path, frame)
    except Exception as e:
        print(f'Error saving image: {e}')
        return False
    return True

def save_frame_as_pdf(frame, timestamp, folder_path):
    # Convert the image to RGB format (assuming it's in BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)

    # Build the PDF file name
    pdf_file_name = f'image_{timestamp}.pdf'
    pdf_file_path = os.path.join(folder_path, pdf_file_name)

    # Save the PIL image as a temporary file
    temp_image_path = os.path.join(folder_path, f'temp_image_{timestamp}.png')
    pil_image.save(temp_image_path)

    # Create a PDF and add the image to it
    pdf = canvas.Canvas(pdf_file_path, pagesize=(rgb_frame.shape[1], rgb_frame.shape[0]))
    pdf.drawImage(temp_image_path, 0, 0, width=rgb_frame.shape[1], height=rgb_frame.shape[0])
    pdf.save()

    # Remove the temporary image file
    os.remove(temp_image_path)

def capture_image(resolution, num_photos, time_delay, image_format):
    # Initialize the camera
    cap = initialize_camera(resolution)

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Create a folder to save the images
    folder_name = 'images'
    folder_path = os.path.join(current_dir, folder_name)
    create_folder(folder_path)

    # Capture the specified number of photos
    for i in range(num_photos):
        # Capture a frame
        ret, frame = cap.read()

        # Get the current date and time in ISO 8601 format
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

        # Build file name with the selected format
        if image_format == 'jpg':
            file_name = f'image_{timestamp}.jpg'
        elif image_format == 'pdf':
            file_name = f'image_{timestamp}.pdf'
            save_frame_as_pdf(frame, timestamp, folder_path)

        image_path = os.path.join(folder_path, file_name)

        # Save the frame based on the selected format
        if not save_image(image_path, frame, timestamp):
            break

        # Show the frame
        cv2.imshow('Frame', frame)

        # Wait the specified time
        time.sleep(time_delay)

        # Break loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

def main():
    # Get the user's resolution, number of photos, waiting time, and image format
    resolution = (1080, 720)
    num_photos = int(input("Enter the number of photos you want to take: "))
    time_delay = float(input("Enter the wait time in seconds between photos: "))
    image_format = input("Enter the image format (jpg or pdf): ").lower()

    # Validate the image format
    while image_format not in ['jpg', 'pdf']:
        print("Invalid image format. Please enter 'jpg' or 'pdf'.")
        image_format = input("Enter the image format (jpg or pdf): ").lower()

    # Capture the images
    capture_image(resolution, num_photos, time_delay, image_format)

if __name__ == "__main__":
    main()
