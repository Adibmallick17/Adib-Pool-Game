import json
from Physics import Coordinate, StillBall, Table, Hole
import os

# Constants
BALL_RADIUS = 28.5  # mm
BALL_DIAMETER = 2 * BALL_RADIUS
HOLE_RADIUS = 2 * BALL_DIAMETER
TABLE_LENGTH = 2700.0  # mm
TABLE_WIDTH = TABLE_LENGTH / 2.0  # mm

def initialize_table_with_balls():
    table = Table()

    # Add the cue ball first
    cue_ball_x = TABLE_WIDTH / 2 - 50  # Adjusted to move the cue ball more to the right
    cue_ball_y = TABLE_LENGTH / 3 + 1400  # Adjusted to move the cue ball further down
    cue_ball_pos = Coordinate(cue_ball_x, cue_ball_y)
    cue_ball = StillBall(0, cue_ball_pos)  # BALLNO set to 0 for the cue ball
    table += cue_ball

    # Set up other balls in a triangle formation
    apex_x = 3 * TABLE_WIDTH / 4 - 300  # Shifted a bit more to the right
    apex_y = TABLE_LENGTH / 3  # Moved up the Y axis
    horizontal_gap = 4  # Adjust as needed for visual clarity
    vertical_gap = 4  # Specifically controls the spacing in the y-axis
    row_length = BALL_DIAMETER + horizontal_gap

    # Loop to place balls in an inverted triangle
    ball_number = 1  # Start numbering the rest of the balls from 1
    for row in range(1, 6):  # 5 rows in the triangle
        for col in range(row):
            pos_x = apex_x - ((row - 1) * row_length / 2) + (col * row_length)
            pos_y = apex_y - ((row - 1) * (BALL_DIAMETER + vertical_gap) * (3**0.5) / 2)
            ball = StillBall(ball_number, Coordinate(pos_x, pos_y))
            table += ball
            ball_number += 1

    # Add holes at the corners
    table += Hole(Coordinate(HOLE_RADIUS, HOLE_RADIUS))  # Top-left
    table += Hole(Coordinate(TABLE_WIDTH - HOLE_RADIUS, HOLE_RADIUS))  # Top-right
    table += Hole(Coordinate(HOLE_RADIUS, TABLE_LENGTH - HOLE_RADIUS))  # Bottom-left
    table += Hole(Coordinate(TABLE_WIDTH - HOLE_RADIUS, TABLE_LENGTH - HOLE_RADIUS))  # Bottom-right

    return table

def save_game_state(table):
    game_state = {
        "table": table.to_json(),  # Ensure your Table class has a to_json() method
    }

    with open('game_state.json', 'w') as f:
        json.dump(game_state, f)

def save_svg(table, filename):
    with open(filename, 'w') as f:
        f.write(table.svg())

if __name__ == "__main__":
    table = initialize_table_with_balls()
    save_svg(table, 'initial_table.svg')