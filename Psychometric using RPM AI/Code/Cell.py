from ImageAnalyzer import *

class Cell:

    def __init__(self, image):
        self.image = image
        self.image_analyzer = ImageAnalyzer()

    def generate_cell_analysis(self):
        self.black_white_ratio = self.image_analyzer.black_white_ratio(self.image)
        self.min_black_distance_l = self.image_analyzer.black_pixel_distance(self.image, "left", "min")
        self.min_black_distance_r = self.image_analyzer.black_pixel_distance(self.image, "right", "min")
        self.min_black_distance_t = self.image_analyzer.black_pixel_distance(self.image, "top", "min")
        self.min_black_distance_b = self.image_analyzer.black_pixel_distance(self.image, "bottom", "min")
        self.max_black_distance_l = self.image_analyzer.black_pixel_distance(self.image, "left", "max")
        self.max_black_distance_r = self.image_analyzer.black_pixel_distance(self.image, "right", "max")
        self.max_black_distance_t = self.image_analyzer.black_pixel_distance(self.image, "top", "max")
        self.max_black_distance_b = self.image_analyzer.black_pixel_distance(self.image, "bottom", "max")
        self.avg_black_distance_l = self.image_analyzer.black_pixel_distance(self.image, "left", "avg")
        self.avg_black_distance_r = self.image_analyzer.black_pixel_distance(self.image, "right", "avg")
        self.avg_black_distance_t = self.image_analyzer.black_pixel_distance(self.image, "top", "avg")
        self.avg_black_distance_b = self.image_analyzer.black_pixel_distance(self.image, "bottom", "avg")


    def get_attrs(self):
        attrs = {}
        attrs['black_white_ratio'] = self.black_white_ratio
        attrs['min_black_distance_l'] = self.min_black_distance_l
        attrs['min_black_distance_r'] = self.min_black_distance_r
        attrs['min_black_distance_t'] = self.min_black_distance_t
        attrs['min_black_distance_b'] = self.min_black_distance_b
        attrs['max_black_distance_l'] = self.max_black_distance_l
        attrs['max_black_distance_r'] = self.max_black_distance_r
        attrs['max_black_distance_t'] = self.max_black_distance_t
        attrs['max_black_distance_b'] = self.max_black_distance_b
        attrs['avg_black_distance_l'] = self.avg_black_distance_l
        attrs['avg_black_distance_r'] = self.avg_black_distance_r
        attrs['avg_black_distance_t'] = self.avg_black_distance_t
        attrs['avg_black_distance_b'] = self.avg_black_distance_b

        return attrs

    # Return percentage difference between cells for each attribute
    def generate_cell_transformation_analysis(self, other_cell):
        transformation = {}
        current_cell_attrs = self.get_attrs()
        for key, value in other_cell.get_attrs().items():
            # If pixel distance is within 2 pixels, consider it 100% the same
            if type(value) == int and current_cell_attrs[key] - value < 3:
                transformation[key] = 1.0
            else:
                transformation[key] = float(current_cell_attrs[key]) / float(value)

        return transformation

    def predict_transformed_attrs(self, transformation_analysis, optional_transformation_analysis = None):
        transformed_attrs = {}
        optional_transformed_attrs = {}
        for key,attr in self.get_attrs().items():
            if optional_transformed_attrs:
                # Return average of predicted BD, CD transformations
                new_value = ((attr * transformation_analysis[key]) + (attr * optional_transformation_analysis[key])) / 2
            else:
                new_value = attr * transformation_analysis[key]
            transformed_attrs[key] = new_value

        return transformed_attrs
