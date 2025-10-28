import open3d as o3d
import pandas as pd
import numpy as np
import argparse

def main(inply, outcsv, sample_n=None, sample_frac=None, seed=0):
    # --- Load PLY ---
    pc = o3d.io.read_point_cloud(inply)

    # --- To arrays ---
    points = np.asarray(pc.points)                       # (N,3)
    colors = np.asarray(pc.colors) if pc.colors else None  # (N,3) in 0..1

    # --- Build DataFrame ---
    if colors is not None and len(colors) == len(points):
        df = pd.DataFrame(
            np.hstack((points, colors)),
            columns=["x", "y", "z", "r", "g", "b"]
        )
        # If you want 0..255 ints instead of 0..1 floats, uncomment:
        # df[["r","g","b"]] = (df[["r","g","b"]] * 255).round().clip(0,255).astype(int)
    else:
        df = pd.DataFrame(points, columns=["x", "y", "z"])

    # --- Random sample (if requested) ---
    if sample_n is not None and sample_frac is not None:
        raise ValueError("Use either --sample_n or --sample_frac, not both.")
    if sample_n is not None:
        sample_n = min(sample_n, len(df))  # safety
        df = df.sample(n=sample_n, random_state=seed)
    elif sample_frac is not None:
        df = df.sample(frac=sample_frac, random_state=seed)

    # --- Save ---
    df.to_csv(outcsv, index=False)
    print(f"Saved {len(df)} points to {outcsv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PLY to CSV; optionally take a random sample.")
    parser.add_argument("-i", "--input_file", type=str, default="export.ply", help="Path to input .ply")
    parser.add_argument("-o", "--output_file", type=str, default="points_use.csv", help="Path to output .csv")
    parser.add_argument("--sample_n", type=int, default=1048576, help="Randomly keep exactly N points")
    parser.add_argument("--sample_frac", type=float, help="Randomly keep this fraction (0<frac<=1)")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for reproducibility")
    args = parser.parse_args()

    main(
        inply=args.input_file,
        outcsv=args.output_file,
        sample_n=args.sample_n,
        sample_frac=args.sample_frac,
        seed=args.seed,
    )

