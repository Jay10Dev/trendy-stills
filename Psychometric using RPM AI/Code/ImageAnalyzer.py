from PIL import Image
from PIL import ImageChops

class ImageAnalyzer:

    def equal_images(self, image1, image2):
        return ImageChops.difference(image1, image2).getbbox() is None

    def root_mean_square_diff(self, image1, image2):
        histogram = ImageChops.difference(image1, image2).histogram()
        sum_of_squares = sum(value*(idx**2) for idx, value in enumerate(histogram))
        root_mean_square_diff = (sum_of_squares/float(image1.size[0] * image2.size[1])) ** 0.5
        return root_mean_square_diff

    def black_white_ratio(self, image):
        pixels = image.getdata()
        nwhite = 0
        for pixel in pixels:
            if pixel == (255, 255, 255, 255):
                nwhite += 1
        n = len(pixels)
        return nwhite / float(n)

    def black_pixel_distance(self, image, direction, metric):
        if direction == "right":
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == "top":
            image = image.rotate(90)
        elif direction == "bottom":
            image = image.rotate(-90)
        pixels = image.load()
        distances = []
        for i in range(0,image.size[0]):
            for j in range(0,image.size[1]):
                pixel = pixels[i,j]
                # If a non-white pixel is reached, return it
                if pixel != (255, 255, 255, 255):
                    distances.append(j)
                    break
        if distances != []:
            if metric == "min":
                return min(distances)
            elif metric == "max":
                return max(distances)
            elif metric == "avg":
                return sum(distances) / len(distances)
        else:
            return 0
