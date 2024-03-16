import cv2
import os
import time
from datetime import datetime
from fpdf import FPDF
import schedule

LOG_MAX_LINES = 1500
LOG_ROTATION_LIMIT = 5

def initialize_camera(resolution_choice):
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Set the resolution based on user's choice
    if resolution_choice == 1:
        resolution = (1080, 800)
    elif resolution_choice == 2:
        resolution = (600, 600)
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

def rotate_logs(log_directory):
    # Get list of log files in the directory
    log_files = sorted([f for f in os.listdir(log_directory) if f.endswith('.log')], reverse=True)

    # Remove excess log files if more than LOG_ROTATION_LIMIT
    if len(log_files) > LOG_ROTATION_LIMIT:
        for file_to_remove in log_files[LOG_ROTATION_LIMIT:]:
            os.remove(os.path.join(log_directory, file_to_remove))

    # Rename log files to make space for a new log
    for i in range(LOG_ROTATION_LIMIT - 1, 0, -1):
        if os.path.exists(os.path.join(log_directory, f"log_{i}.log")):
            os.rename(os.path.join(log_directory, f"log_{i}.log"), os.path.join(log_directory, f"log_{i+1}.log"))

    # Rename current log to log_1.log
    if os.path.exists(os.path.join(log_directory, "log.log")):
        os.rename(os.path.join(log_directory, "log.log"), os.path.join(log_directory, "log_1.log"))

def log(message):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_directory = os.path.join(script_dir, 'logs')

    # Rotate logs if necessary
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    rotate_logs(log_directory)

    # Write to current log file
    with open(os.path.join(log_directory, "log.log"), "a") as log_file:
        log_file.write(f"{datetime.now().isoformat()} - {message}\n")

def capture_image(resolution_choice, num_photos, time_delay, image_format):
    # Initialize the camera
    cap, resolution = initialize_camera(resolution_choice)

    # Create a folder to save the images
    image_folder = create_image_folder()

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

    # Capture the specified number of photos
    for i in range(num_photos - 1):
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

def capture_images_scheduled(resolution_choice, num_photos, time_delay, image_format):
    # Capture an immediate photo
    capture_image(resolution_choice, num_photos, time_delay, image_format)

    # Schedule image capture every 3 minutes
    schedule.every(3).minutes.do(capture_image, resolution_choice, num_photos, time_delay, image_format)

    # Run the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    while True:
        # Get the number of photos
        num_photos = int(input("Enter the number of photos you want to take (maximum 10): "))

        # Check if the number of photos exceeds the maximum limit
        if num_photos > 10:
            print("Error: Number of photos exceeds the maximum limit of 10. Please enter a valid number.")
        else:
            break  # Exit the loop if the number is valid

    # Get resolution choice from user
    resolution_choice = get_resolution_choice()

    # Get the waiting time between photos
    while True:
        # Get the waiting time between photos
        time_delay = float(input("Enter the wait time in seconds between photos (maximum 5 seconds): "))

        # Check if the time delay exceeds the maximum limit
        if time_delay > 5:
            print("Error: Time delay exceeds the maximum limit of 5 seconds. Please enter a valid time.")
        else:
            break  # Exit the loop if the time delay is valid

    # Get the image format
    image_format = input("Enter the image format (jpg or pdf): ").lower()

    # Validate the image format
    while image_format not in ['jpg', 'pdf']:
        print("Invalid image format. Please enter 'jpg' or 'pdf'.")
        image_format = input("Enter the image format (jpg or pdf): ").lower()

    # Capture the initial photo and schedule subsequent captures
    capture_images_scheduled(resolution_choice, num_photos, time_delay, image_format)

if __name__ == "__main__":
    main()