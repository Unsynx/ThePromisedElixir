from PIL import Image


def cut_sprite_sheet(input_path, output_folder):
    # Open the sprite sheet image
    sprite_sheet = Image.open(input_path)

    # Get the dimensions of the sprite sheet
    sheet_width, sheet_height = sprite_sheet.size

    # Define the size of each individual sprite
    sprite_size = 128

    # Calculate the number of sprites in each row and column
    num_sprites_x = sheet_width // sprite_size
    num_sprites_y = sheet_height // sprite_size

    # Cut the sprite sheet into individual sprites
    for y in range(num_sprites_y):
        for x in range(num_sprites_x):
            left = x * sprite_size
            upper = y * sprite_size
            right = left + sprite_size
            lower = upper + sprite_size

            # Crop the sprite from the sprite sheet
            sprite = sprite_sheet.crop((left, upper, right, lower))

            # Save the individual sprite
            output_path = f"{output_folder}/tile_{y * num_sprites_x + x + 1}.png"
            sprite.save(output_path)


# Thanks ChatGPT
if __name__ == "__main__":
    # Replace 'input_sprite_sheet.png' with the path to your sprite sheet image
    input_path = '../assets/tiles/wall_back-Sheet.png'

    # Replace 'output_folder' with the folder where you want to save the individual sprites
    output_folder = 'out'

    cut_sprite_sheet(input_path, output_folder)
