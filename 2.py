from PIL import Image
import numpy as np

def edit_image(path, operation, value=None, save_as="output.jpg", path2=None):
    img = Image.open(path)
    arr = np.array(img)

    if operation == "grayscale":
        R, G, B = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        result = (0.299*R + 0.587*G + 0.114*B).astype(np.uint8)

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
        h, w = arr.shape[0], arr.shape[1]
        arr2 = np.array(img2.resize((w, h)))
        weight = float(value) if value is not None else 0.5
        result = arr.astype(float)*weight + arr2.astype(float)*(1-weight)
        result = np.clip(result, 0, 255).astype(np.uint8)

    elif operation == "blur":
        arr_f = arr.astype(float)
        up    = np.roll(arr_f, -1, axis=0)
        down  = np.roll(arr_f, 1, axis=0)
        left_ = np.roll(arr_f, -1, axis=1)
        right_= np.roll(arr_f, 1, axis=1)
        result = (arr_f + up + down + left_ + right_) / 5
        result = np.clip(result, 0, 255).astype(np.uint8)

    else:
        raise ValueError(f"Unknown operation: {operation}")

    Image.fromarray(result).save(save_as)
    print(f"Saved: {save_as}")
    return result





def run():
    path = input("Image path: ").strip()

    while True:
        word = input("\nType an operation (grayscale/brightness/contrast/flip_h/flip_v/crop/invert/blend/blur, or 'quit'): ").strip().lower()

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