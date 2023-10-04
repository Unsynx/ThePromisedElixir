import os
import random


def generate_dungeon(chunk_size):
    # Delete current world
    dir_name = "../assets/world"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".txt"):
            os.remove(os.path.join(dir_name, item))

    # Create world
    width = 10
    height = 10

    world = []
    for y in range(height * chunk_size):
        row = []
        for x in range(width * chunk_size):
            row.append(random.randint(0, 1))

        world.append(row)

    # Save chunks to files
    for h in range(height):
        for w in range(width):
            with open(f"../assets/world/chunk_{w}_{h}.txt", "x") as f:
                for i in range(chunk_size):
                    row = world[(h * chunk_size) + i - 1][(chunk_size * w):(chunk_size * (w+1))]
                    for c, li in enumerate(list(map(str, row))):
                        if c != 0:
                            f.write(", ")
                        f.write(f"{li}")
                    f.write("\n")


generate_dungeon(4)
