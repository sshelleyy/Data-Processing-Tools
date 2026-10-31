import hyperspectral_interpolation as hi_metrics
import numpy as np
import matplotlib.pyplot as plt


def generate_spectral_viz(ref_cube, rec_cube, pixel_coords=None):
    """
    Visualizes spectral signature comparison for a specific pixel.
    """
    # Use center pixel if coords aren't provided
    y, x = (
        pixel_coords
        if pixel_coords
        else (ref_cube.shape[0] // 2, ref_cube.shape[1] // 2)
    )

    ref_sig = ref_cube[y, x, :]
    rec_sig = rec_cube[y, x, :]

    plt.figure(figsize=(10, 6))
    plt.plot(ref_sig, label="Original", color="blue")
    plt.plot(rec_sig, label="Upscaled", color="orange", linestyle="--")

    plt.title(f"Spectral Signature Comparison | Pixel: ({x}, {y})")
    plt.xlabel("Band Index")
    plt.ylabel("Intensity")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.savefig("spectral_comparison.png", dpi=300)
    plt.show()


# run
original_path = "/Users/shelley/Desktop/pythonFiles/utatOnboarding/three-dimensions/sample-data-cubes/indian-pine-files/indian_pine_array.npy"
og_lowres_path = "/Users/shelley/Desktop/pythonFiles/utatOnboarding/three-dimensions/sample-data-cubes/indian-pine-files/resized_IPA.npy"
upscaled_path = "/Users/shelley/Desktop/pythonFiles/utatOnboarding/three-dimensions/sample-data-cubes/indian-pine-files/upscaled_IPA.npy"

original = np.load(original_path)

# loading shape. if odd num pixels, crop
h, w, b = original.shape
if h % 2 != 0 or w % 2 != 0:
    original = original[: h - (h % 2), : w - (w % 2), :]
    print(f"Cropped to {original.shape}")

np.save(og_lowres_path, original[::2, ::2, :])
og_lowres = np.load(og_lowres_path)

# resize

hi_metrics.upscale_hyperspectral(og_lowres_path, upscaled_path)
upscaled = np.load(upscaled_path)

generate_spectral_viz(original, upscaled)
