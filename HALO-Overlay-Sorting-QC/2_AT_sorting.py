import pygame
import os
from PIL import Image

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
AI_labeled_image_as = True

# Set directories for images
unsorted_folder = ".../1_sort/" # point to the folder with images that need to be sorted
positive_folder_path = ".../2_sort_pos/" # point to the folder where you want + cells saved
negative_folder_path = '.../2_sort_neg/' # point to the folder where you want - cells saved
skipped_folder_path = '.../2_sort_skipped/' # point to the folder where you want skipped images saved

def load_image(image_path):
    try:
        original_image = pygame.image.load(image_path)
        image = pygame.transform.scale(original_image, (original_image.get_width() * 1.5, original_image.get_height() * 1.5))
        return image
    except pygame.error as e:
        print("Unable to load image:", image_path)
        raise SystemExit(e)


def display_image(image, x, y):
    screen.blit(image, (x, y))
    pygame.display.flip()


def main():
    AI_pos_count = 0
    AI_neg_count = 0

    true_pos_count = 0
    true_neg_count = 0

    false_pos_count = 0
    false_neg_count = 0
    skipped_count = 0

    # Get list of image files in folders
    unsorted_images = [f for f in os.listdir(unsorted_folder) if os.path.isfile(os.path.join(unsorted_folder, f))]
    total_images = len(unsorted_images)

    # Initial image index + count
    current_image_index = 0
    sorted_count = 0

    # Load first image + set folder
    current_folder = unsorted_folder
    current_image = load_image(os.path.join(current_folder, unsorted_images[current_image_index]))


    # Set image position + size
    image_x = (SCREEN_WIDTH - current_image.get_width()) // 4
    image_y = (SCREEN_HEIGHT - current_image.get_height()) // 4

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                file_name = unsorted_images[current_image_index]
                #record if the AI thought the cell was + or -
                AI_labeled_image_as = False
                if "marked_pos" in file_name:
                    AI_pos_count += 1
                    AI_labeled_image_as = True
                if "marked_neg" in file_name:
                    AI_neg_count += 1
                    AI_labeled_image_as = False

                # If the user presses right arrow key, they say the cell is positive
                # If the AI agrees, true pos, if the AI disagreed, false negative
                if event.key == pygame.K_RIGHT:
                    if "marked_pos" in file_name:
                        true_pos_count += 1
                    if "marked_neg" in file_name:
                        false_neg_count += 1

                    print(f"{file_name} was sorted as + ({sorted_count}/{total_images})")

                    #save image to positive cell folder
                    pygame.image.save(current_image, os.path.join(positive_folder_path, unsorted_images[current_image_index]))
                    # Move to next image
                    current_image_index = (current_image_index + 1) % len(unsorted_images)
                    current_image = load_image(os.path.join(unsorted_folder, unsorted_images[current_image_index]))
                    sorted_count += 1

                # If the user presses left arrow key, they say the cell is negative
                # If the AI agrees, true pos, if the AI disagreed, false negative
                elif event.key == pygame.K_LEFT:
                    print(f"{file_name} was sorted as - ({sorted_count}/{total_images})")
                    if "marked_pos" in file_name:
                        false_pos_count += 1
                    if "marked_neg" in file_name:
                        true_neg_count += 1

                    #save image in the negative folder for sorting
                    pygame.image.save(current_image, os.path.join(negative_folder_path, unsorted_images[current_image_index]))


                    # Move to next image
                    current_image_index = (current_image_index + 1) % len(unsorted_images)
                    current_image = load_image(os.path.join(unsorted_folder, unsorted_images[current_image_index]))
                    sorted_count += 1

                # If the user presses spacebar, skip the image
                elif event.key == pygame.K_SPACE:
                    print(f"{file_name} was skipped ({sorted_count}/{total_images})")

                    skipped_count+=1
                    pygame.image.save(current_image, os.path.join(skipped_folder_path, unsorted_images[current_image_index]))

                    # Move to next image
                    current_image_index = (current_image_index + 1) % len(unsorted_images)
                    current_image = load_image(os.path.join(unsorted_folder, unsorted_images[current_image_index]))
                    sorted_count += 1

                # conditions to exit the loop
                elif event.key == pygame.K_ESCAPE:
                    running = False
                if sorted_count == total_images:
                    running = False

        screen.fill(BLACK)
        display_image(current_image, image_x, image_y)
        pygame.display.update()


    pygame.quit()
    print(f"AI pos count: {AI_neg_count}\n"
          f"AI neg count: {AI_neg_count}\n"
          f"AI true positive count: {true_pos_count}\n"
          f"AI true negative count: {true_neg_count}\n"
          f"False + count: {false_pos_count}\n"
          f"False - count: {false_neg_count}\n"
          f"Skipped count: {skipped_count}\n")
    if AI_pos_count > 0:
        print(f"False + %: {100*(false_pos_count/AI_pos_count)}%\n")
    if AI_neg_count>0:
        print(f"False - %: {100 * (false_neg_count / AI_neg_count)}%")




if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Right Arrow: +, Left Arrow: -, Spacebar: Skip")
    main()
