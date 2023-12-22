#!/usr/bin/python3

from tqdm import tqdm


def get_next_steps(grid, origin_steps, infinite_grid=False):
    new_steps = set()
    for step in origin_steps:
        for neighbor in [
            (step[0] - 1, step[1]),
            (step[0] + 1, step[1]),
            (step[0], step[1] - 1),
            (step[0], step[1] + 1),
        ]:
            if infinite_grid:
                map_row = neighbor[0] % len(grid)
                map_col = neighbor[1] % len(grid[0])
            else:
                map_row = neighbor[0]
                map_col = neighbor[1]
                if not (0 <= map_row < len(grid)) or not (
                    0 <= map_col < len(grid[0]) - 1
                ):
                    continue
            if grid[map_row][map_col] == ".":
                new_steps.add(neighbor)
    return new_steps


def part1(grid, start_node):
    step_nodes = [start_node]
    for _ in range(64):
        step_nodes = get_next_steps(grid, step_nodes)
    return len(step_nodes)


def part2(grid, start_node):
    # Basic flow:
    # 1. Gather Initial Data
    #       Naively count visited tiles for two periods, where period is
    #       defined as the length of the grid. This only works because the
    #       grid has all sides free of obstacles. This was also crudely
    #       confirmed by plotting the deltas (gradient) of each step with
    #       pyplot.
    #
    # 2. Calculate Delta Coefficients
    #       We have one full period captured from above. As we process the
    #       second period, save the linear coefficients that relate the
    #       deltas to the delta in the same spot in the previous cycle.
    #
    # 3. Extrapolate Final Expansion
    #       With the linear coefficients above, we can calculate how much
    #       delta is expected between steps without actually counting.
    #       Incrementally update the total using these calculated deltas.
    #
    # NOTES:
    #       This does NOT work on the test data and I don't know why not.
    #       I could find out by analyzing the plot of the cycles but this
    #       problem has taken long enough and this works for the correct
    #       answer for the actual input.
    deltas = [0]
    delta_coefficients = []
    step_nodes = [start_node]
    tile_count = 0
    period = len(grid)

    for i in tqdm(range(2 * period), desc="Gathering initial data"):
        step_nodes = get_next_steps(grid, step_nodes, True)
        deltas.append(len(step_nodes) - tile_count)
        tile_count = len(step_nodes)

    for i in tqdm(
        range(2 * period, 3 * period + 1), desc="Calculating delta coefficients"
    ):
        step_nodes = get_next_steps(grid, step_nodes, True)
        deltas.append(len(step_nodes) - tile_count)
        tile_count = len(step_nodes)

        # Save coefficients for linear delta equations
        m = (deltas[i + 1] - deltas[i - period + 1]) / period
        b = deltas[i + 1] - m * i
        delta_coefficients.append((m, b))

    for i in tqdm(
        range(3 * period + 1, 26501365), desc="Extrapolating final expansion"
    ):
        # We have enough data to extrapolate the deltas
        eq = delta_coefficients[i % period]
        delta = round(eq[0] * i + eq[1])
        tile_count += delta
    return tile_count


grid = []
row = 0
start_node = None
with open("input.txt", "r") as f:
    for line in f:
        si = line.find("S")
        if si > -1:
            start_node = (row, si)
            line = line.replace("S", ".")
        grid.append(list(line.rstrip()))
        row += 1

print(f"Part 1: {part1(grid, start_node)}")
print(f"Part 2: {part2(grid, start_node)}")
