import itertools
import random

# Global variable to track the minimum score across all paths
min_score = float('inf')

def roll_dice_sequence(max_rolls, use_two_dice=True):
    # Generate a sequence of dice rolls
    rolls = []
    for _ in range(max_rolls):
        if use_two_dice:
            rolls.append(random.randint(1, 6) + random.randint(1, 6))
        else:
            rolls.append(random.randint(1, 6))
    return rolls

def find_combinations(target, numbers):
    # Find all combinations of numbers that sum up to the target
    combinations = []
    for i in range(1, len(numbers) + 1):
        for combo in itertools.combinations(numbers, i):
            if sum(combo) == target:
                combinations.append(combo)
    return combinations

def simulate_game(board, two_dice_sequence, one_die_sequence, two_dice_index=0, one_die_index=0, path=[]):
    global min_score

    # Check if all numbers are covered (i.e., the game is won)
    if all(board):
        return [(0, path)]

    # Determine which sequence to use
    if all(board[6:12]):  # 7-12 are covered, use one die sequence
        use_two_dice = False
    else:
        use_two_dice = True

    # Select the appropriate roll sequence
    if use_two_dice:
        if two_dice_index >= len(two_dice_sequence):
            # If we run out of rolls, calculate the score
            score = sum(i + 1 for i in range(12) if not board[i])
            min_score = min(min_score, score)
            return [(score, path)]
        roll_sum = two_dice_sequence[two_dice_index]
        roll_index = two_dice_index
    else:
        if one_die_index >= len(one_die_sequence):
            # If we run out of rolls, calculate the score
            score = sum(i + 1 for i in range(12) if not board[i])
            min_score = min(min_score, score)
            return [(score, path)]
        roll_sum = one_die_sequence[one_die_index]
        roll_index = one_die_index

    available_numbers = [i + 1 for i in range(12) if not board[i]]
    valid_combinations = find_combinations(roll_sum, available_numbers)

    if not valid_combinations:
        # No valid combinations, return the score
        score = sum(i + 1 for i in range(12) if not board[i])
        min_score = min(min_score, score)
        return [(score, path)]

    results = []
    # Try each combination as a separate branch
    for combination in valid_combinations:
        new_board = board[:]
        new_path = path + [combination]
        for number in combination:
            new_board[number - 1] = True

        # Recurse into the next roll with the new board state
        if use_two_dice:
            results.extend(simulate_game(new_board, two_dice_sequence, one_die_sequence, roll_index + 1, one_die_index, new_path))
        else:
            results.extend(simulate_game(new_board, two_dice_sequence, one_die_sequence, two_dice_index, roll_index + 1, new_path))
    
    return results

def play_all_paths(max_rolls=20):
    # Initialize the board: 1-12 all uncovered
    initial_board = [False] * 12

    # Generate fixed sequences of rolls
    two_dice_sequence = roll_dice_sequence(max_rolls, use_two_dice=True)
    one_die_sequence = roll_dice_sequence(max_rolls, use_two_dice=False)
    
    print(f"Two dice roll sequence: {two_dice_sequence}")
    print(f"One die roll sequence: {one_die_sequence}")

    # Simulate the game with the fixed roll sequences
    results = simulate_game(initial_board, two_dice_sequence, one_die_sequence)

    # Output results
    for score, path in results:
        print(f"Path: {path}, Score: {score}.")

def simulate_games(num_simulations, max_rolls=20):
    global min_score

    for _ in range(num_simulations):
        print("Simulation:")
        
        # Reset min_score for each simulation
        min_score = float('inf')
        
        play_all_paths(max_rolls)
        
        # Display the minimum score found in the current simulation
        print(f"Minimum Score in Simulation: {min_score}.")
        print("=" * 40)
    return min_score

# Run the simulation and print results
index = 0
num = 3
count = 0
while min_score > num or count < 10:
    index += 1
    if (simulate_games(1) <= num):
        count += 1
print(f"{index} Simulations elapsed. Count is {count}")
