from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

def average_pixel_values_circle(image_path):
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)
    # Get the height and width of the image
    height, width = image_array.shape
    # Calculate the size of each part
    part_height = height // 3
    part_width = width // 3
    radius = min(part_height, part_width) // 2

    average_values = []

    # Divide the image into 9 parts and calculate the average pixel value of the largest circle in each part
    for i in range(3):
        for j in range(3):
            part = image_array[i*part_height:(i+1)*part_height, j*part_width:(j+1)*part_width]
            center_x, center_y = part_width // 2, part_height // 2

            # Create a mask for the circle
            mask = np.zeros((part_height, part_width), dtype=bool)
            y, x = np.ogrid[:part_height, :part_width]
            distance = (x - center_x)**2 + (y - center_y)**2
            mask[distance <= radius**2] = True

            # Calculate the average pixel value within the circle
            circle_pixels = part[mask]
            average_value = np.mean(circle_pixels)
            average_values.append(average_value)
    
    return average_values

if __name__ == "__main__":
    file_paths = [
        "samples/4-0.jpg",
        "samples/1-2.jpg",
        "samples/2-1.jpg",
        "samples/3-1.jpg"
    ]

    THRESHOLD = 100

    results = {}

    for file_path in file_paths:
        results[file_path] = average_pixel_values_circle(file_path)

    for image, averages in results.items():
        name = image.split("/")[-1].replace("jpg", "")
        matrix = np.array(averages).reshape(3, 3)
        print(matrix)

        plt.imshow(matrix, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title('Heatmap of 3x3 Matrix')

        # To generate heatmaps uncomment the line below.
        # plt.savefig(f'heatmap-{name}.png')

        for index, average in enumerate(averages):
            y = (index // 3)
            x = (index % 3)


            if average <= THRESHOLD:
                print(image, x + 1, y + 1)