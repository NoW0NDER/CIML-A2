import sys, random, grader, parse, math, copy

from p2 import get_p_action_space, move_pacman

def to_string(problem):
    current_map = copy.deepcopy(problem.game_map)
    for key in problem.loc_map:
        x, y = problem.loc_map[key]
        current_map[x][y] = key
    return '\n'.join([''.join(row) for row in current_map])

def get_ghost_action_space(state,ghost):
    forbidden = {"%"}.union(set(state.loc_map.keys()))
    forbidden.remove('P')
    ghost_action_space = []
    other_ghost_loc = []
    for g in state.loc_map:
        if g != ghost and g != 'P':
            other_ghost_loc.append(state.loc_map[g])
    if state.game_map[state.loc_map[ghost][0]][state.loc_map[ghost][1]+1] not in forbidden and (state.loc_map[ghost][0], state.loc_map[ghost][1]+1) not in other_ghost_loc:
        ghost_action_space.append('E')
    if state.game_map[state.loc_map[ghost][0]-1][state.loc_map[ghost][1]] not in forbidden and (state.loc_map[ghost][0]-1, state.loc_map[ghost][1]) not in other_ghost_loc:
        ghost_action_space.append('N')
    if state.game_map[state.loc_map[ghost][0]+1][state.loc_map[ghost][1]] not in forbidden and (state.loc_map[ghost][0]+1, state.loc_map[ghost][1]) not in other_ghost_loc:
        ghost_action_space.append('S')
    if state.game_map[state.loc_map[ghost][0]][state.loc_map[ghost][1]-1] not in forbidden and (state.loc_map[ghost][0], state.loc_map[ghost][1]-1) not in other_ghost_loc:
        ghost_action_space.append('W')
    return ghost_action_space

def move_ghost(problem, action, ghost):
    if action == 'E':
        problem.loc_map[ghost] = (problem.loc_map[ghost][0], problem.loc_map[ghost][1]+1)
    elif action == 'N':
        problem.loc_map[ghost] = (problem.loc_map[ghost][0]-1, problem.loc_map[ghost][1])
    elif action == 'S':
        problem.loc_map[ghost] = (problem.loc_map[ghost][0]+1, problem.loc_map[ghost][1])
    elif action == 'W':
        problem.loc_map[ghost] = (problem.loc_map[ghost][0], problem.loc_map[ghost][1]-1)
    if problem.loc_map['P'] == problem.loc_map[ghost]:
        problem.game_map[problem.loc_map['P'][0]][problem.loc_map['P'][1]] = ' '
        problem.loc_map.pop('P')
        problem.score -= 500
        return True
    return False


def random_play_multiple_ghosts(problem):
    #Your p3 code here
    random.seed(problem.seed,version=1)
    res=""
    res+=f"seed: {problem.seed}\n"
    step_counter = 0
    res+=f"{step_counter}\n"
    res+=to_string(problem)+'\n'
    
    while True:
        step_counter+=1
        if "P" not in problem.loc_map:
            res+=f"score: {problem.score}\n"
            res+="WIN: Ghost"
            break
        p_action_space = get_p_action_space(problem)
        if len(p_action_space) == 0:
            res+=f"{step_counter}\n"
            res+=to_string(problem)+'\n'
            res+=f"score: {problem.score}\n"
            res+="WIN: Ghost"
            break
        action = random.choice(p_action_space)
        res+=f"{step_counter}: P moving {action}\n"
        if move_pacman(problem, action):
            res+=to_string(problem)+'\n'
            res+=f"score: {problem.score}\n"
            if problem.score > 0:
                res+="WIN: Pacman"
            else:
                res+="WIN: Ghost"
            break
        res+=to_string(problem)+'\n'
        res+=f"score: {problem.score}\n"
        for ghost in sorted(problem.loc_map):
            if ghost == 'P':
                continue
            step_counter+=1
            g_action_space = get_ghost_action_space(problem, ghost)
            if len(g_action_space) == 0:
                res+=f"{step_counter}: {ghost} moving \n"
                res+=to_string(problem)+'\n'
                res+=f"score: {problem.score}\n"
                continue
            action = random.choice(g_action_space)
            res+=f"{step_counter}: {ghost} moving {action}\n"
            
            if move_ghost(problem, action, ghost):
                # res+=to_string(problem)+'\n'
                res+=to_string(problem)+'\n'
                break
            res+=to_string(problem)+'\n'
            res+=f"score: {problem.score}\n"
        else:
            continue
        
        
    
    solution = res
    return solution

if __name__ == "__main__":
    try: test_case_id = int(sys.argv[1])
    except: test_case_id = -7
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)