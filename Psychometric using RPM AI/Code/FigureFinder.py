from ImageAnalyzer import *

class FigureFinder:

    def __init__(self):
        self.image_analyzer = ImageAnalyzer()

    def find_matching_figure_filename(self, example_figure, solution_figures):
        example_figure_file = example_figure.visualFilename
        example_figure_image = Image.open(example_figure_file)
        for figure in solution_figures:
            fileName = figure.visualFilename
            figureImage = Image.open(fileName)
            if self.image_analyzer.root_mean_square_diff(example_figure_image, figureImage) < 965:
                return fileName

    def find_matching_y_flipped_figure_filename(self, example_figure, solution_figures):
        example_figure_file = example_figure.visualFilename
        example_figure_image = Image.open(example_figure_file).transpose(Image.FLIP_LEFT_RIGHT)
        for figure in solution_figures:
            fileName = figure.visualFilename
            figureImage = Image.open(fileName)
            if self.image_analyzer.root_mean_square_diff(example_figure_image, figureImage) < 965:
                return fileName

    def find_matching_x_flipped_figure_filename(self, example_figure, solution_figures):
        example_figure_file = example_figure.visualFilename
        example_figure_image = Image.open(example_figure_file).transpose(Image.FLIP_TOP_BOTTOM)
        for figure in solution_figures:
            fileName = figure.visualFilename
            figureImage = Image.open(fileName)
            if self.image_analyzer.root_mean_square_diff(example_figure_image, figureImage) < 965:
                return fileName
