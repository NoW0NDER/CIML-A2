import sys, parse, random
import time, os, copy

# from p2 import get_p_action_space, move_pacman
from p3 import get_ghost_action_space, move_ghost, get_p_action_space, move_pacman

def to_string(problem):
    current_map = copy.deepcopy(problem.game_map)
    for key in problem.loc_map:
        x, y = problem.loc_map[key]
        current_map[x][y] = key
    return '\n'.join([''.join(row) for row in current_map])

def eval_state_action(state,action):
    p_y = state.loc_map['P'][0]
    p_x = state.loc_map['P'][1]
    ghost_locs = []
    for g in state.loc_map:
        if g != 'P':
            w_y = state.loc_map[g][0]
            w_x = state.loc_map[g][1]
            ghost_locs.append((w_y,w_x))
    if action == 'E':
        p_x += 1
    elif action == 'N':
        p_y -= 1
    elif action == 'W':
        p_x -= 1
    elif action == 'S':
        p_y += 1
    if (p_y,p_x) in ghost_locs:
        return -1000
    else:
        ghost_score = 1/(min([abs(p_x - w_x) + abs(p_y - w_y) for w_y,w_x in ghost_locs])+sum([abs(p_x - w_x) + abs(p_y - w_y) for w_y,w_x in ghost_locs])/len(ghost_locs))
        dot_distances = [abs(p_x - dot[0]) + abs(p_y - dot[1]) for dot in state.dots]
        if len(dot_distances) == 0:
            dot_distances = [1]
        action_score = 0
        if min(dot_distances) == 0:
            action_score += 3
        else:
            action_score += 1/(min(dot_distances)+1)
        total_score = action_score - ghost_score
        return total_score
            
def choose_best_action(state,action_space):
    best_action = action_space[0]
    best_score = -1000
    for action in action_space:
        score = eval_state_action(state,action)
        if score > best_score:
            best_score = score
            best_action = action
    return best_action


def reflex_play_multiple_ghosts(problem, verbose):
    #Your p4 code here
    
    solution = ''
    winner = ''
    
    solution+=f"seed: {problem.seed}\n"
    step_counter = 0
    solution+=f"{step_counter}\n"
    solution+=to_string(problem)+'\n'
    while True:
        step_counter+=1
        if "P" not in problem.loc_map:
            solution+=f"score: {problem.score}\n"
            solution+="WIN: Ghost"
            winner = 'Ghost'
            break
        p_action_space = get_p_action_space(problem)
        if len(p_action_space) == 0:
            solution+=f"{step_counter}\n"
            solution+=to_string(problem)+'\n'
            solution+=f"score: {problem.score}\n"
            solution+="WIN: Ghost"
            winner = 'Ghost'
            break
        action = choose_best_action(problem,p_action_space)
        solution+=f"{step_counter}: P moving {action}\n"
        if move_pacman(problem, action):
            solution+=to_string(problem)+'\n'
            solution+=f"score: {problem.score}\n"
            if problem.score > 0:
                winner = 'Pacman'
            break
        solution+=to_string(problem)+'\n'
        solution+=f"score: {problem.score}\n"
        for ghost in sorted(problem.loc_map):
            if ghost == 'P':
                continue
            step_counter+=1
            g_action_space = get_ghost_action_space(problem, ghost)
            if len(g_action_space) == 0:
                solution+=f"{step_counter}: {ghost} moving \n"
                solution+=to_string(problem)+'\n'
                solution+=f"score: {problem.score}\n"
                continue
            action = random.choice(g_action_space)
            solution+=f"{step_counter}: {ghost} moving {action}\n"
            
            if move_ghost(problem, action, ghost):
                # res+=to_string(problem)+'\n'
                solution+=to_string(problem)+'\n'
                break
            solution+=to_string(problem)+'\n'
            solution+=f"score: {problem.score}\n"
        else:
            continue
        
    if verbose:
        print(solution)
    return solution, winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 4
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
        solution, winner = reflex_play_multiple_ghosts(copy.deepcopy(problem), verbose)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)