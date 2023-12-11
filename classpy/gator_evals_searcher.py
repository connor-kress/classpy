from PIL import Image
import os


def gator_evals_searcher(folder_path: os.PathLike, input_name: str) -> bool:
    # Rearrange the input name from "First Last" to "Last_First"
    name_parts = input_name.split()
    if len(name_parts) == 2:
        search_name = f"{name_parts[1]}_{name_parts[0]}".lower()
    else:
        print("Please enter the name in 'First Last' format.")
        return False

    # Search for an image with the rearranged name
    for file in os.listdir(folder_path):
        if file.lower().startswith(search_name) and \
            file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(folder_path, file)
            with Image.open(image_path) as img:
                img.show()
            return True

    # If no matching image is found
    print(f"No image found for '{input_name}'.")
    return False


def main() -> None:
    folder_path = input("Enter the path of the folder: ")
    input_name = input("Enter the name as 'First Last': ")
    gator_evals_searcher(folder_path, input_name)


if __name__ == '__main__':
    main()
