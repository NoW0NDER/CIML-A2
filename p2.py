import sys, random , parse
import time, os, copy
import math
from p1 import to_string    



def get_p_action_space(state):
    forbidden = {"%"}.union(set(state.loc_map.keys()))
    p_action_space = []
    # print(state.loc_map['P'])
    if state.game_map[state.loc_map['P'][0]][state.loc_map['P'][1]+1] not in forbidden:
        p_action_space.append('E')
    if state.game_map[state.loc_map['P'][0]-1][state.loc_map['P'][1]] not in forbidden:
        p_action_space.append('N')
    if state.game_map[state.loc_map['P'][0]+1][state.loc_map['P'][1]] not in forbidden:
        p_action_space.append('S')
    if state.game_map[state.loc_map['P'][0]][state.loc_map['P'][1]-1] not in forbidden:
        p_action_space.append('W')
    return p_action_space

def get_ghost_action_space(state):
    forbidden = {"%"}.union(set(state.loc_map.keys()))
    forbidden.remove('P')
    ghost_action_space = []
    if state.game_map[state.loc_map['W'][0]][state.loc_map['W'][1]+1] not in forbidden:
        ghost_action_space.append('E')
    if state.game_map[state.loc_map['W'][0]-1][state.loc_map['W'][1]] not in forbidden:
        ghost_action_space.append('N')
    if state.game_map[state.loc_map['W'][0]+1][state.loc_map['W'][1]] not in forbidden:
        ghost_action_space.append('S')
    if state.game_map[state.loc_map['W'][0]][state.loc_map['W'][1]-1] not in forbidden:
        ghost_action_space.append('W')
    return ghost_action_space


def eval_state_action(state,action):
    p_y = state.loc_map['P'][0]
    p_x = state.loc_map['P'][1]
    w_y = state.loc_map['W'][0]
    w_x = state.loc_map['W'][1]
    if action == 'E':
        p_x += 1
    elif action == 'N':
        p_y -= 1
    elif action == 'W':
        p_x -= 1
    elif action == 'S':
        p_y += 1
    distance_to_ghost = abs(p_x - w_x) + abs(p_y - w_y)
    dot_distances = [abs(p_x - dot[0]) + abs(p_y - dot[1]) for dot in state.dots]
    if len(dot_distances) == 0:
        dot_distances = [1]
    action_score = 0
    if distance_to_ghost<2:
        action_score -= distance_to_ghost/2
    if min(dot_distances) == 0:
        action_score += 3
    else:
        action_score += 1/(min(dot_distances)+1)
    return action_score
def get_p_action(state, action_space):
    action_score_dict = dict()
    # print(action_space)
    for action in action_space:
        action_score_dict[action] = eval_state_action(state,action)
    best_action = max(action_score_dict, key=action_score_dict.get)
    # print(action_score_dict)
    # print(best_action)
    return best_action


def move_pacman(state, action):
    state.score -= 1
    if action == 'E':
        state.loc_map['P'] = (state.loc_map['P'][0], state.loc_map['P'][1]+1)
    elif action == 'N':
        state.loc_map['P'] = (state.loc_map['P'][0]-1, state.loc_map['P'][1])
    elif action == 'S':
        state.loc_map['P'] = (state.loc_map['P'][0]+1, state.loc_map['P'][1])
    elif action == 'W':
        state.loc_map['P'] = (state.loc_map['P'][0], state.loc_map['P'][1]-1)
    if state.game_map[state.loc_map['P'][0]][state.loc_map['P'][1]] == '.':
        state.dot_count -= 1
        state.dots.remove((state.loc_map['P'][0], state.loc_map['P'][1]))
        state.score += 10
        state.game_map[state.loc_map['P'][0]][state.loc_map['P'][1]] = ' '
        if state.dot_count == 0:
            state.score += 500
            return True
    for g in state.loc_map:
        if g != 'P':
            if state.loc_map['P'] == state.loc_map[g]:
                state.game_map[state.loc_map['P'][0]][state.loc_map['P'][1]] = ' '
                state.loc_map.pop('P')
                state.score -= 500
                return True
    # if state.loc_map['P'] == state.loc_map['W']:
    #     state.game_map[state.loc_map['P'][0]][state.loc_map['P'][1]] = ' '
    #     state.loc_map.pop('P')
    #     state.score -= 500
    #     return True
    return False


def random_play_single_ghost(state):
    g_action_space = get_ghost_action_space(state)
    g_action = random.choice(g_action_space)
    if g_action == 'E':
        state.loc_map['W'] = (state.loc_map['W'][0], state.loc_map['W'][1]+1)
    elif g_action == 'N':
        state.loc_map['W'] = (state.loc_map['W'][0]-1, state.loc_map['W'][1])
    elif g_action == 'S':
        state.loc_map['W'] = (state.loc_map['W'][0]+1, state.loc_map['W'][1])
    elif g_action == 'W':
        state.loc_map['W'] = (state.loc_map['W'][0], state.loc_map['W'][1]-1)
    if state.loc_map['P'] == state.loc_map['W']:
        state.game_map[state.loc_map['P'][0]][state.loc_map['P'][1]] = ' '
        state.loc_map.pop('P')
        state.score -= 500
        return True
    return False
        
    
    

def reflex_play_single_ghost(problem, verbose):
    #Your p2 code here
    solution = ''
    winner = 'Ghost'
    while True:
        # print(to_string(problem))
        p_action_space = get_p_action_space(problem)
        if len(p_action_space) == 0:
            break
        action = get_p_action(problem, p_action_space)
        if move_pacman(problem, action):
            if problem.score > 0:
                winner = 'Pacman'
            break
        if random_play_single_ghost(problem):
            break
    solution += to_string(problem) + '\n'
    solution += f"score: {problem.score}\n"
    if winner == 'Pacman':
        solution += "WIN: Pacman"
    else:
        solution += "WIN: Ghost"
    if verbose:
        print(solution)
        
    

    return solution, winner

if __name__ == "__main__":
    #random.seed(0)
    test_case_id = int(sys.argv[1])    
    problem_id = 2
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        #print(i)
        solution, winner = reflex_play_single_ghost(copy.deepcopy(problem), verbose)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time:',end - start)
    print('win %',win_p)