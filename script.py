import cv2
import os
import time
from datetime import datetime
from fpdf import FPDF

def initialize_camera(resolution_choice):
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Set the resolution based on user's choice
    if resolution_choice == 1:
        resolution = (1080, 800)
    elif resolution_choice == 2:
        resolution = (600, 600)
    else:
        print("Invalid resolution choice. Defaulting to (1080, 800).")
        resolution = (1080, 800)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    return cap, resolution

def create_image_folder():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create a folder to save the images
    image_folder = os.path.join(script_dir, 'images')
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    return image_folder

def save_image(image_path, frame, image_format):
    # Save the frame as an image
    try:
        if image_format == 'jpg':
            cv2.imwrite(image_path, frame)
        elif image_format == 'pdf':
            # Save the frame as a temporary image file
            temp_image_path = os.path.splitext(image_path)[0] + '.jpg'
            cv2.imwrite(temp_image_path, frame)

            # Create a PDF and add the image to it
            pdf = FPDF()
            pdf.add_page()
            pdf.image(temp_image_path, x=0, y=0, w=210, h=297)  # Assuming A4 page size
            pdf.output(image_path)
            os.remove(temp_image_path)
    except Exception as e:
        print(f'Error saving image: {e}')


def capture_image(resolution_choice, num_photos, time_delay, image_format):
    # Initialize the camera
    cap, resolution = initialize_camera(resolution_choice)

    # Create a folder to save the images
    image_folder = create_image_folder()

    # Capture the specified number of photos
    for i in range(num_photos):
        # Capture a frame
        ret, frame = cap.read()

        # Get the current date and time in ISO 8601 format
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

        # Build file name with the selected format
        file_name = f'image_{timestamp}.{image_format}'
        image_path = os.path.join(image_folder, file_name)

        # Save the frame
        save_image(image_path, frame, image_format)

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
    
def get_resolution_choice():
    # Show resolution options
    print("Resolution Options:")
    print("1. 1080x800")
    print("2. 600x600")
    
    # Get resolution choice from user
    while True:
        resolution_choice = input("Enter the number for your desired resolution: ")
        if resolution_choice in ['1', '2']:
            return int(resolution_choice)
        else:
            print("Invalid resolution choice. Please enter '1' or '2'.")

def main():
    # Get the number of photos, waiting time, resolution, and image format
    num_photos = int(input("Enter the number of photos you want to take: "))
    resolution_choice = get_resolution_choice()
    time_delay = float(input("Enter the wait time in seconds between photos: "))
    image_format = input("Enter the image format (jpg or pdf): ").lower()

    # Validate the image format
    while image_format not in ['jpg', 'pdf']:
        print("Invalid image format. Please enter 'jpg' or 'pdf'.")
        image_format = input("Enter the image format (jpg or pdf): ").lower()

    # Capture the images
    capture_image(resolution_choice, num_photos, time_delay, image_format)

if __name__ == "__main__":
    main()
