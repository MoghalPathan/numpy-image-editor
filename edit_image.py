from PIL import Image
import numpy as np

def edit_image(path, operation, value=None, save_as="output.jpg", path2=0):
    img = Image.open(path)
    arr = np.array(img)

    if operation == "grayscale":
        """
        R = arr[:, :, 0]         
        G = arr[:, :, 1]
        B = arr[:, :, 2]
        u can use both

        """

        R,G,B=arr[:,:,0], arr[:,:,1], arr[:,:,2]      
        result = (0.299 * R + 0.587 * G + 0.114 * B).astype(np.uint8)

    elif operation == "brightness":
        result = arr.astype(int) + int(value)
        result = np.clip(result, 0, 255).astype(np.uint8) 

    elif operation == "contrast":
        result = (arr.astype(int) - 128) * float(value) + 128
        result = np.clip(result, 0, 255).astype(np.uint8) 

    elif operation == "flip_h":
        result = arr[:, ::-1] 

    elif operation == "flip_v":
        result = arr[::-1, :]

    elif operation == "crop":
        top, bottom, left, right = [int(x) for x in value.split(",")]
        result = arr[top:bottom, left:right]

    elif operation == "invert":
        result = 255 - arr 

    elif operation == "blend":
        img2 = Image.open(path2)
        height, width = arr.shape[0], arr.shape[1]
        img2_resized = img2.resize((width, height))   
        arr2 = np.array(img2_resized)

        weight = float(value) if value is not None else 0.5
        result = arr.astype(float)*weight + arr2.astype(float)*(1-weight) 
        result = np.clip(result, 0, 255).astype(np.uint8)

    elif operation == "blur":
        arr_f = arr.astype(float)
        up = np.roll(arr_f, -10, axis=0)
        down = np.roll(arr_f, 10, axis=0)
        left = np.roll(arr_f, -10, axis=1)
        right = np.roll(arr_f, 10, axis=1)

        result = (arr_f + up + down + left + right)/ 5
        result = np.clip(result, 0, 255).astype(np.uint8)

    else:
            raise ValueError(f"Unknown operation: {operation}")

    Image.fromarray(result).save(save_as)
    print(f"Saved: {save_as}\n")
    return result

ALIASES = {
    "gray": "grayscale", "grayscale": "grayscale", "greyscale": "grayscale",
    "bright": "brightness", "brightness": "brightness",
    "contrast": "contrast",
    "fliph": "flip_h", "flip_h": "flip_h", "fliphorizontal": "flip_h",
    "flipv": "flip_v", "flip_v": "flip_v", "flipvertical": "flip_v",
    "crop": "crop",
    "invert": "invert",
    "blend": "blend",
    "blur": "blur",
}
NEEDS_VALUE = {"brightness", "contrast", "crop", "blend"}

def run():
    path = input("Image path:").strip()

    while True:
        word = input("Type an operation: ").strip().lower()

        if word == "quit":
            break

        if word not in ALIASES:
            print("Didn't recognize that word, try again.")
            continue

        operation = ALIASES[word]
        value = None
        path2 = None

        if operation in NEEDS_VALUE:
            if operation == "brightness":
                value = input("  Amount to add (e.g. 40): ").strip()
            elif operation == "contrast":
                value = input("  Contrast factor (e.g. 1.5): ").strip()
            elif operation == "crop":
                value = input("  top,bottom,left,right (e.g. 100,300,200,500): ").strip()
            elif operation == "blend":
                path2 = input("  Second image path: ").strip()
                value = input("  Blend weight 0-1 (e.g. 0.5): ").strip()

        save_as = f"out_{operation}.jpg"
        edit_image(path, operation, value=value, save_as=save_as, path2=path2)                


if __name__ == "__main__":
     run()         