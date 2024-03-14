import sys, random, grader, parse, copy

def to_string(problem):
    current_map = copy.deepcopy(problem.game_map)
    for key in problem.loc_map:
        x, y = problem.loc_map[key]
        current_map[x][y] = key
    return '\n'.join([''.join(row) for row in current_map])


def random_play_single_ghost(problem):
    #Your p1 code here
    random.seed(problem.seed, version=1)
    step_counter = 0
    score  = 0
    solution = f'seed: {problem.seed}\n'
    solution += f"{step_counter}\n"
    solution += to_string(problem) + '\n'
    forbidden = {"%"}
    
    while problem.dot_count > 0:
        # if step_counter > 50:
        #     break
        P_action_space = []
        if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]+1] !="%":
            P_action_space.append('E')
        if problem.game_map[problem.loc_map['P'][0]-1][problem.loc_map['P'][1]] !="%":
            P_action_space.append('N')
        if problem.game_map[problem.loc_map['P'][0]+1][problem.loc_map['P'][1]] !="%":
            P_action_space.append('S')
        if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]-1] !="%":
            P_action_space.append('W')
        action = random.choice(P_action_space)
        score -= 1
        step_counter += 1
        solution += f"{step_counter}: P moving {action}\n"
        if action == 'E':
            problem.loc_map['P'] = (problem.loc_map['P'][0], problem.loc_map['P'][1]+1)
            if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] == '.':
                problem.dot_count -= 1
                score+=10
                problem.dots.remove((problem.loc_map['P'][0], problem.loc_map['P'][1]))
            if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] == 'W':
                problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]-1] = ' '
                problem.loc_map.pop('P')
                score -= 500
                solution += to_string(problem) + '\n'
                solution += f"score: {score}\n"
                solution += "WIN: Ghost"
                break
            problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] = 'P'
            problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]-1] = ' '
        elif action == 'N':
            problem.loc_map['P'] = (problem.loc_map['P'][0]-1, problem.loc_map['P'][1])
            if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] == '.':
                problem.dot_count -= 1
                score+=10
                problem.dots.remove((problem.loc_map['P'][0], problem.loc_map['P'][1]))
                
            if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] == 'W':
                problem.game_map[problem.loc_map['P'][0]+1][problem.loc_map['P'][1]] = ' '
                problem.loc_map.pop('P')
                score -= 500
                solution += to_string(problem) + '\n'
                solution += f"score: {score}\n"
                solution += "WIN: Ghost"
                break
            problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] = 'P'
            problem.game_map[problem.loc_map['P'][0]+1][problem.loc_map['P'][1]] = ' '
        elif action == 'S':
            problem.loc_map['P'] = (problem.loc_map['P'][0]+1, problem.loc_map['P'][1])
            if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] == '.':
                problem.dot_count -= 1
                score+=10
                problem.dots.remove((problem.loc_map['P'][0], problem.loc_map['P'][1]))
                
            if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] == 'W':
                problem.game_map[problem.loc_map['P'][0]-1][problem.loc_map['P'][1]] = ' '
                problem.loc_map.pop('P')
                score -= 500
                solution += to_string(problem) + '\n'
                solution += f"score: {score}\n"
                solution += "WIN: Ghost"
                break
            problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] = 'P'
            problem.game_map[problem.loc_map['P'][0]-1][problem.loc_map['P'][1]] = ' '
        elif action == 'W':
            problem.loc_map['P'] = (problem.loc_map['P'][0], problem.loc_map['P'][1]-1)
            if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] == '.':
                problem.dot_count -= 1
                score+=10
                problem.dots.remove((problem.loc_map['P'][0], problem.loc_map['P'][1]))
                
            if problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] == 'W':
                problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]+1] = ' '
                problem.loc_map.pop('P')
                score -= 500
                solution += to_string(problem) + '\n'
                solution += f"score: {score}\n"
                solution += "WIN: Ghost"
                break
            problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] = 'P'
            problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]+1] = ' '
        solution += f"{to_string(problem)}\n"
        if problem.dot_count == 0:
            score += 500
            solution += f"score: {score}\n"
            solution += "WIN: Pacman"
            break
        solution += f"score: {score}\n"
        W_action_space = []
        if problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]+1] not in forbidden:
            W_action_space.append('E')
        if problem.game_map[problem.loc_map['W'][0]-1][problem.loc_map['W'][1]] not in forbidden:
            W_action_space.append('N')
        if problem.game_map[problem.loc_map['W'][0]+1][problem.loc_map['W'][1]] not in forbidden:
            W_action_space.append('S')
        if problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]-1] not in forbidden:
            W_action_space.append('W')
        action = random.choice(W_action_space)
        step_counter += 1
        solution += f"{step_counter}: W moving {action}\n"
        if action == 'E':
            problem.loc_map['W'] = (problem.loc_map['W'][0], problem.loc_map['W'][1]+1)
            problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]-1] = 'W'
            if (problem.loc_map['W'][0], problem.loc_map['W'][1]-1) in problem.dots:
                problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]-1] = '.'
            else:
                problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]-1] = ' '
        elif action == 'N':
            problem.loc_map['W'] = (problem.loc_map['W'][0]-1, problem.loc_map['W'][1])
            problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]] = 'W'
            if (problem.loc_map['W'][0]+1, problem.loc_map['W'][1]) in problem.dots:
                problem.game_map[problem.loc_map['W'][0]+1][problem.loc_map['W'][1]] = '.'
            else:
                problem.game_map[problem.loc_map['W'][0]+1][problem.loc_map['W'][1]] = ' '
        elif action == 'S':
            problem.loc_map['W'] = (problem.loc_map['W'][0]+1, problem.loc_map['W'][1])
            problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]] = 'W'
            if (problem.loc_map['W'][0]-1, problem.loc_map['W'][1]) in problem.dots:
                problem.game_map[problem.loc_map['W'][0]-1][problem.loc_map['W'][1]] = '.'
            else:
                problem.game_map[problem.loc_map['W'][0]-1][problem.loc_map['W'][1]] = ' '
        elif action == 'W':
            problem.loc_map['W'] = (problem.loc_map['W'][0], problem.loc_map['W'][1]-1)
            problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]] = 'W'
            if (problem.loc_map['W'][0], problem.loc_map['W'][1]+1) in problem.dots:
                problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]+1] = '.'
            else:
                problem.game_map[problem.loc_map['W'][0]][problem.loc_map['W'][1]+1] = ' '
        
        if problem.loc_map['P'] == problem.loc_map['W']:
            problem.loc_map.pop('P')
            solution += f"{to_string(problem)}\n"
            score -= 500
            solution += f"score: {score}\n"
            solution += "WIN: Ghost"
            break
        else:
            solution += f"{to_string(problem)}\n"
            solution += f"score: {score}\n"
        
            
            
                
        
            
    
    
    
    
    
    return solution

if __name__ == "__main__":
    try: test_case_id = int(sys.argv[1])
    except: test_case_id = -6
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)