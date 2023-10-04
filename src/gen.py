import random


def generate_dungeon(chunk_size):
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
                    row = world[chunk_size + (h * chunk_size) - 1][(chunk_size * w):(chunk_size * (w+1))]
                    for li in list(map(str, row)):
                        f.write(f"{li}, ")
                    f.write("\n")


generate_dungeon(4)
