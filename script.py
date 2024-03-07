import cv2
import os
import time
from datetime import datetime
from fpdf import FPDF

def capture_image(resolution, num_photos, time_delay, image_format):
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Set the resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # Full path to desktop directory
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'images')

    # Create a folder to save the images
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    # Capture the specified number of photos
    for i in range(num_photos):
        # Capture a frame
        ret, frame = cap.read()

        # Get the current date and time in ISO 8601 format
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

        # Build file name with the selected format
        if image_format == 'jpg':
            file_name = f'image_{timestamp}.jpg'
            image_path = os.path.join(desktop_path, file_name)

            # Save the frame as an image
            try:
                cv2.imwrite(image_path, frame)
            except Exception as e:
                print(f'Error saving image: {e}')
                return
        elif image_format == 'pdf':
            # Save the frame as a temporary image file
            temp_image_path = os.path.join(desktop_path, 'temp_image.jpg')
            cv2.imwrite(temp_image_path, frame)

            # Create a PDF and add the image to it
            pdf = FPDF()
            pdf.add_page()
            pdf.image(temp_image_path, x=0, y=0, w=210, h=297)  # Assuming A4 page size
            pdf_file_name = f'image_{timestamp}.pdf'
            pdf_file_path = os.path.join(desktop_path, pdf_file_name)
            pdf.output(pdf_file_path)

            # Remove the temporary image file
            os.remove(temp_image_path)

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
