class ProblemHelper:
    def is_two_by_two_problem(self, problem):
        return len(problem.figures) == 9

    def get_problem_figures(self, problem):
        problem_figures = []
        possible_files = ['A.png', 'B.png', 'C.png', 'D.png', 'E.png', 'F.png', 'G.png', 'H.png']
        for figureName in problem.figures:
            thisFigure = problem.figures[figureName]
            fileName = thisFigure.visualFilename
            if fileName[-5:] in possible_files:
                problem_figures.append(thisFigure)
        return problem_figures

    def get_solution_figures(self, problem):
        solution_figures = []
        possible_files = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
        for figureName in problem.figures:
            thisFigure = problem.figures[figureName]
            fileName = thisFigure.visualFilename
            if fileName[-5:] in possible_files:
                solution_figures.append(thisFigure)
        return solution_figures
