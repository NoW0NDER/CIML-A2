import os, sys

class Problem:
    def __init__(self, seed, game_map, loc_map,dot_count,dots):
        self.seed = seed
        self.game_map = game_map
        self.loc_map = loc_map
        self.dot_count = dot_count
        self.dots = dots
        self.score = 0

def read_layout_problem(file_path):
    #Your p1 code here
    
    with open(file_path, 'r') as file:
        seed = int(file.readline().strip().split()[1])
        game_map = []
        loc_map = dict()
        dot_count = 0
        dots = set()
        while True:
            line = file.readline().strip()
            if not line:
                break
            
            game_map.append([])
            for token in line:
                if token == '%':
                    game_map[-1].append("%")
                elif token == '.':
                    game_map[-1].append(".")
                    dot_count += 1
                    dots.add((len(game_map)-1, len(game_map[-1])-1))
                elif token == " ":
                    game_map[-1].append(" ")
                else:
                    game_map[-1].append(" ")
                    loc_map[token] = (len(game_map)-1, len(game_map[-1])-1)
    
        problem = Problem(seed, game_map, loc_map,dot_count,dots)
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')