from PIL import Image
from PIL import ImageChops
from Cell import *
from FigureFinder import *
from ProblemHelper import *

class Agent:

    def __init__(self):
        pass

    def Solve(self,problem):
        problem_helper = ProblemHelper()
        answer = -1
        # Solve 2x2 problems
        if problem_helper.is_two_by_two_problem(problem):
            two_by_two_solver = TwoByTwoProblemSolver(problem)
            answer = two_by_two_solver.high_level_analsis()
            if answer != -1:
                return answer # Return answer if high level analysis succeeds
            # Otherwise, perform a deeper analysis
            answer = two_by_two_solver.detailed_transformation_analysis()
        if answer:
            return answer
        else:
            return -1

class TwoByTwoProblemSolver:

    def __init__(self, problem):
        self.image_analyzer = ImageAnalyzer()
        self.problem = problem

    # Check for case where A,B,C are all equal
    def check_all_equal_figures(self, problem_figures):
        cell_images = []
        for figure in problem_figures:
            fileName = figure.visualFilename
            figureImage = Image.open(fileName)
            cell_images.append(figureImage)
        for i in range(len(cell_images)-1):
            if not self.image_analyzer.root_mean_square_diff(cell_images[i], cell_images[i+1]) < 965:
                return False
        return True

    # Check for case where A and B are equal
    def check_equal_ab_figures(self, problem_figures):
        cell_images = {}
        for figure in problem_figures:
            fileName = figure.visualFilename
            figureImage = Image.open(fileName)
            cell_images[fileName[-5]] = figureImage
        if self.image_analyzer.root_mean_square_diff(cell_images['A'], cell_images['B']) < 965:
            return True
        else:
            return False

    # Check for case where A and C are equal
    def check_equal_ac_figures(self, problem_figures):
        cell_images = {}
        for figure in problem_figures:
            fileName = figure.visualFilename
            figureImage = Image.open(fileName)
            cell_images[fileName[-5]] = figureImage
        if self.image_analyzer.root_mean_square_diff(cell_images['A'], cell_images['C']) < 965:
            return True
        else:
            return False

    # Checks if image is flipped on it's y-axis when crossing the y-axis of the matrix
    def check_y_axis_flip(self, problem_figures):
        cell_images = {}
        for figure in problem_figures:
            fileName = figure.visualFilename
            figureImage = Image.open(fileName)
            cell_images[fileName[-5]] = figureImage
        # Check if flipping figure A across the y-axis produces figure B
        if self.image_analyzer.root_mean_square_diff(cell_images['A'].transpose(Image.FLIP_LEFT_RIGHT), cell_images['B']) < 965:
            return True
        else:
            return False

    # Checks if image is flipped on it's x-axis when crossing the x-axis of the matrix
    def check_x_axis_flip(self, problem_figures):
        cell_images = {}
        for figure in problem_figures:
            fileName = figure.visualFilename
            figureImage = Image.open(fileName)
            cell_images[fileName[-5]] = figureImage
        # Check if flipping figure A across the y-axis produces figure C
        if self.image_analyzer.root_mean_square_diff(cell_images['A'].transpose(Image.FLIP_TOP_BOTTOM), cell_images['C']) < 965:
            return True
        else:
            return False

    # Perform 5 checks for very basic 2x2 patterns
    def high_level_analsis(self):
        problem_helper = ProblemHelper()
        problem_figures = problem_helper.get_problem_figures(self.problem)
        solution_figures = problem_helper.get_solution_figures(self.problem)
        figure_finder = FigureFinder()

        # Check for all equal figures case
        if self.check_all_equal_figures(problem_figures):
            solution_figure_filename = figure_finder.find_matching_figure_filename(problem_figures[0], solution_figures) # Pass in any figure
            if solution_figure_filename:
                solution_number = solution_figure_filename[-5] # Get image number from filename string
                return int(solution_number)

        # Check for AB equal
        if self.check_equal_ab_figures(problem_figures):
            for f in problem_figures:
                if "C.png" in f.visualFilename:
                    solution_figure_filename = figure_finder.find_matching_figure_filename(f, solution_figures) # Pass in figure C

                    # If proposed solution figure is present, return the number of that image
                    if solution_figure_filename:
                        solution_number = int(solution_figure_filename[-5]) # Get image number from filename string
                        return solution_number

        # Check for AC equal
        if self.check_equal_ac_figures(problem_figures):
            for f in problem_figures:
                if "B.png" in f.visualFilename:
                    solution_figure_filename = figure_finder.find_matching_figure_filename(f, solution_figures) # Pass in figure C

                    # If proposed solution figure is present, return the number of that image
                    if solution_figure_filename:
                        solution_number = int(solution_figure_filename[-5]) # Get image number from filename string
                        return solution_number

        # Check for simple y-axis flip transformation
        if self.check_y_axis_flip(problem_figures):
            for f in problem_figures:
                if "C.png" in f.visualFilename:
                    solution_figure_filename = figure_finder.find_matching_y_flipped_figure_filename(f, solution_figures) # Pass in figure C

                    # If proposed solution figure is present, return the number of that image
                    if solution_figure_filename:
                        solution_number = int(solution_figure_filename[-5]) # Get image number from filename string
                        return solution_number

        # Check for simple x-axis flip transformation
        if self.check_x_axis_flip(problem_figures):
            for f in problem_figures:
                if "B.png" in f.visualFilename:
                    solution_figure_filename =  figure_finder.find_matching_x_flipped_figure_filename(f, solution_figures) # Pass in figure B

                    # If proposed solution figure is present, return the number of that image
                    if solution_figure_filename:
                        solution_number = int(solution_figure_filename[-5]) # Get image number from filename string
                        return solution_number

        return -1

    # Remove solution cells that do not match the observed patterns
    def sift_solution_cells(self, solution_cells, patterns):
        sifted_solution_cells = solution_cells
        for p_key, pattern in patterns.items():
            for s_key, solution in solution_cells.items():
                solution_attrs = solution.get_attrs()
                valid = False
                # If solution cell attribute is equal to the pattern, add it to sifted_solution_cells
                if round(solution_attrs[p_key], 5) == round(pattern,5):
                    valid = True
                else:
                    # Otherwise, if solution is a very close int, consider it acceptable
                    if type(solution_attrs[p_key]) == int:
                        if solution_attrs[p_key] == pattern+1 or solution_attrs[p_key] == pattern+2:
                            valid = True
                        if solution_attrs[p_key] == pattern-1 or solution_attrs[p_key] == pattern-2:
                            valid = True
                    # Otherwise, solution is missing a pattern, so remove it
                    if valid == False:
                        sifted_solution_cells.pop(s_key, None)

        return sifted_solution_cells

    def generate_similarity_score(self, solution_attrs, d_expected_attributes):
        scores = []
        for s_key, s_attr in solution_attrs.items():
            # Ignore cases where values are 0
            if s_attr == 0 or d_expected_attributes[s_key] == 0:
                continue
            attr_score = s_attr / d_expected_attributes[s_key]
            scores.append(attr_score)
        total_score = sum(scores) / len(scores)

        return total_score

    def analyze_transformation_patterns(self, problem_cells, attributes):
        transformation_patterns = {}
        abc_pattern = {}
        ab_pattern = {}
        ac_pattern = {}
        for attr in attributes:
            a_value = problem_cells['a'].get_attrs()[attr]
            b_value = problem_cells['b'].get_attrs()[attr]
            c_value = problem_cells['c'].get_attrs()[attr]

            # Check for ABC pattern
            if a_value == b_value == c_value:
                abc_pattern[attr] = a_value
            else:
                # Otherwise, check for AB or AC patterns
                if a_value == b_value:
                    ab_pattern[attr] = c_value # Expect C value in cell D
                elif a_value == c_value:
                    ac_pattern[attr] = b_value # Expect B value in cell D

            # Secondary check for close enough values
            if type(a_value) == int: # Check for close enough pixel distances
                if (a_value == b_value+1 == c_value+1 or a_value == b_value-1 == c_value-1
                    or a_value == b_value+1 == c_value-1 or a_value == b_value-1 == c_value+1
                    or a_value == b_value+2 == c_value+2 or a_value == b_value-2 == c_value-2
                    or a_value == b_value+2 == c_value-2 or a_value == b_value-2 == c_value+2):
                    abc_pattern[attr] = a_value
                else:
                    if (a_value == b_value or a_value == b_value+1 or a_value == b_value-1
                        or a_value == b_value+2 or a_value == b_value-2):
                        ab_pattern[attr] = c_value # Expect C value in cell D
                    elif (a_value == c_value or a_value == c_value+1 or a_value == c_value-1
                        or a_value == c_value+2 or a_value == c_value-2):
                        ac_pattern[attr] = b_value # Expect B value in cell D
            else: # Check for close enough black/white ratios
                if round(a_value,5) == round(b_value,5) == round(c_value,5):
                    abc_pattern[attr] = a_value
                else:
                    if round(a_value,5) == round(b_value,5):
                        ab_pattern[attr] = c_value # Expect C value in cell D
                    elif round(a_value,5) == round(c_value,5):
                        ac_pattern[attr] = b_value # Expect B value in cell D
        transformation_patterns['abc'] = abc_pattern
        transformation_patterns['ab'] = ab_pattern
        transformation_patterns['ac'] = ac_pattern

        return transformation_patterns


    # Performs detailed analysis on multiple images attributes and how they
    # transform between cells.  Returns proposed solution number if certainty
    # is above the appropriate threshold, otherwise returns -1.
    def detailed_transformation_analysis(self):
        problem_helper = ProblemHelper()
        problem_figures = problem_helper.get_problem_figures(self.problem)
        solution_figures = problem_helper.get_solution_figures(self.problem)

        ATTRIBUTES = ['black_white_ratio', 'min_black_distance_l', 'min_black_distance_r',
                      'min_black_distance_t', 'min_black_distance_b', 'max_black_distance_l',
                      'max_black_distance_r', 'max_black_distance_t', 'max_black_distance_b',
                      'avg_black_distance_l', 'avg_black_distance_r','avg_black_distance_t',
                      'avg_black_distance_b' ]

        # Instantiate A,B,C cells with their images
        problem_cells = {}
        for figure in problem_figures:
            if "A.png" in figure.visualFilename:
                problem_cells['a'] = Cell(Image.open(figure.visualFilename))
            elif "B.png" in figure.visualFilename:
                problem_cells['b'] = Cell(Image.open(figure.visualFilename))
            elif "C.png" in figure.visualFilename:
                problem_cells['c'] = Cell(Image.open(figure.visualFilename))

        # Instantiate 1-6 cells with their images
        solution_cells = {}
        for figure in solution_figures:
            if "1.png" in figure.visualFilename:
                solution_cells['1'] = Cell(Image.open(figure.visualFilename))
            elif "2.png" in figure.visualFilename:
                solution_cells['2'] = Cell(Image.open(figure.visualFilename))
            elif "3.png" in figure.visualFilename:
                solution_cells['3'] = Cell(Image.open(figure.visualFilename))
            elif "4.png" in figure.visualFilename:
                solution_cells['4'] = Cell(Image.open(figure.visualFilename))
            elif "5.png" in figure.visualFilename:
                solution_cells['5'] = Cell(Image.open(figure.visualFilename))
            elif "6.png" in figure.visualFilename:
                solution_cells['6'] = Cell(Image.open(figure.visualFilename))

        # Generate an image analysis for each problem cell
        for _, problem_cell in problem_cells.items():
            problem_cell.generate_cell_analysis()

        # Generate an image analysis for each solution cell
        for _, solution_cell in solution_cells.items():
            solution_cell.generate_cell_analysis()

        # Find ABC, AB, AC transformations where attributes remain close to the same
        transformation_patterns = self.analyze_transformation_patterns(problem_cells, ATTRIBUTES)
        abc_pattern = transformation_patterns['abc']
        ab_pattern = transformation_patterns['ab']
        ac_pattern = transformation_patterns['ac']

        # If any ABC attribute or AB, AC transormation attribute remains exactly
        # the same, that attributes value should be expected in the solution.
        # Remove possible solutions cells that do not match these patterns.
        unsifted_cells = dict(solution_cells)
        sifted_solution_cells = self.sift_solution_cells(unsifted_cells, abc_pattern) # Sift for ABC pattern
        sifted_solution_cells = self.sift_solution_cells(sifted_solution_cells, ab_pattern) # Sift for AB pattern
        sifted_solution_cells = self.sift_solution_cells(sifted_solution_cells, ac_pattern) # Sift for AC pattern
        if not sifted_solution_cells:
            sifted_solution_cells = solution_cells

        # Generate analyses for AB, AC transformations
        ab_transformation_analysis = problem_cells['a'].generate_cell_transformation_analysis(problem_cells['b'])
        ac_transformation_analysis = problem_cells['a'].generate_cell_transformation_analysis(problem_cells['b'])

        # Predict the attributes of D that AD, BD, CD transformations will
        # produce based on the observed AB, AC transformations
        ab_ac_transform_applied_to_a = problem_cells['a'].predict_transformed_attrs(ab_transformation_analysis, ac_transformation_analysis)
        ac_transform_applied_to_b = problem_cells['b'].predict_transformed_attrs(ac_transformation_analysis)
        ab_transform_applied_to_c = problem_cells['c'].predict_transformed_attrs(ab_transformation_analysis)

        d_expected_attributes = {}
        for attr in ATTRIBUTES:
            total = ab_ac_transform_applied_to_a[attr] + ac_transform_applied_to_b[attr] + ab_transform_applied_to_c[attr]
            average = total / 3
            d_expected_attributes[attr] = average

        # Generate similarity scores for each sifted solution compared to the
        # average expected attributes of D
        similarity_scores = {}
        for key,solution in sifted_solution_cells.items():
            solution_attrs = solution.get_attrs()
            similarity_score = self.generate_similarity_score(solution_attrs, d_expected_attributes)
            similarity_scores[key] = similarity_score

        # Choose the solution with the highest similarity score
        proposed_solution = int(max(similarity_scores, key=similarity_scores.get))
        similarity = similarity_scores[str(proposed_solution)]

        # If the combined similarity score is above the 95% threshold, then
        # return the number of the proposed solution cell, otherwise, if we
        # can sift out enough solutions, return the solution with the highest
        # similarity score, otherwise, return -1
        if proposed_solution and similarity > 0.95:
            return proposed_solution
        elif len(sifted_solution_cells) < 5:
            return proposed_solution
        else:
            return -1
