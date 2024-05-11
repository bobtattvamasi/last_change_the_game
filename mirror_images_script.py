# just script for mirror images
from PIL import Image


def mirror_images(folder_path, animation_images):
    """
    Mirrors the provided animation images and saves them with a "_left" suffix.

    Args:
        folder_path (str): Path to the folder containing the animation images.
        animation_images (list): List of filenames representing the animation images.
    """

    for image_name in animation_images:
        # Create full image path
        image_path = f"{folder_path}/{image_name}"

        # Open image
        image = Image.open(image_path)

        # Mirror the image
        mirrored_image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # Create mirrored image filename
        mirrored_filename = f"{folder_path}/{image_name.split('.')[0]}_left.{image_name.split('.')[1]}"

        # Save the mirrored image
        mirrored_image.save(mirrored_filename)


# Example usage (replace with your actual folder path and image list)
# folder_path = "images/enemy/dino"
# animation_images = ["idle1.png", "run1.png", "run2.png", "run3.png", "run4.png", "run5.png", "run6.png",
#                     "run7.png", "run8.png", "dead.png"]
# folder_path = "images/enemy/ghosts/pix_ghost"
# animation_images = ["idle1.png", "run1.png", "run2.png", "dead.png"]

folder_path = "images/enemy/bat"
animation_images = ["idle1.png", "bat_fly.png", "bat_hang.png", "dead.png"]
mirror_images(folder_path, animation_images)

print("Mirrored images saved successfully!")