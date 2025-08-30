'''
point cloud data is stored as a 2D matrix
each row has 3 values i.e. the x, y, z value for a point

Project has to be submitted to github in the private folder assigned to you
Readme file should have the numerical values as described in each task
Create a folder to store the images as described in the tasks.
'''
#%%
import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa

#%% utility functions
def show_cloud(points_plt):
    ax = plt.axes(projection='3d')
    ax.scatter(points_plt[:,0], points_plt[:,1], points_plt[:,2], s=0.01)
    plt.show()

def show_scatter(x,y):
    plt.scatter(x, y)
    plt.show()

def get_ground_level(points: np.ndarray,
                     bins: int = 256,
                     low_pct: float = 0.5,
                     high_pct: float = 95.0) -> float:
    # get z column
    z = points[:, -1].astype(float)
    z = z[np.isfinite(z)]
    if z.size == 0:
        raise ValueError("No finite z values in point cloud")

    # clip outliers
    lo = np.percentile(z, low_pct)
    hi = np.percentile(z, high_pct)
    zc = z[(z >= lo) & (z <= hi)]
    if zc.size == 0:
        zc = z  # fallback

    # histogram on clipped z
    hist, edges = np.histogram(zc, bins=bins)
    centers = 0.5 * (edges[:-1] + edges[1:])

    # prefer the lower 30% of the range (ground is low)
    low_end = zc.min()
    high_end = low_end + 0.30 * (zc.max() - low_end)
    mask = (centers >= low_end) & (centers <= high_end)

    # take peak (mode)
    if np.any(mask):
        peak_idx = np.where(mask)[0][np.argmax(hist[mask])]
    else:
        peak_idx = int(np.argmax(hist))

    return float(centers[peak_idx])

def save_histogram(points: np.ndarray, g: float, tag: str, out_dir: str = "plots"):
    os.makedirs(out_dir, exist_ok=True)
    z = points[:, -1].astype(float)
    plt.figure(figsize=(7,4))
    plt.hist(z, bins=256)
    plt.axvline(g, color="red", linestyle="--", linewidth=2)
    plt.title(f"{tag}: height histogram\nEstimated ground level = {g:.3f}")
    plt.xlabel("Height (z)")
    plt.ylabel("Count")
    out_path = os.path.join(out_dir, f"{tag}_hist.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"{tag} ground level: {g:.6f}  (saved {out_path})")

#%% ==== TASK 1 ====
# Load both datasets
pcd1 = np.load(r"e:\Documents\LNU\Summer 1\IT Lulea\Ass 5\Lidar_processing\dataset1.npy")
pcd2 = np.load(r"e:\Documents\LNU\Summer 1\IT Lulea\Ass 5\Lidar_processing\dataset2.npy")

# Compute ground levels
g1 = get_ground_level(pcd1)
g2 = get_ground_level(pcd2)

# Save histograms
save_histogram(pcd1, g1, "dataset1", out_dir="plots")
save_histogram(pcd2, g2, "dataset2", out_dir="plots")

# View of clouds
show_cloud(pcd1)
show_cloud(pcd2)
