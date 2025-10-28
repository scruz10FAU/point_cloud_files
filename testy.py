import open3d as o3d, numpy as np
pc = o3d.io.read_point_cloud("export.ply")
P = np.asarray(pc.points)
print("Y min/max:", P[:,1].min(), P[:,1].max())
print("Pct with y<0:", (P[:,1] < 0).mean()*100, "%")
print("X min/max:", P[:,0].min(), P[:,0].max())
print("Pct with x<0:", (P[:,0] < 0).mean()*100, "%")
print("Z min/max:", P[:,2].min(), P[:,2].max())
print("Pct with z<0:", (P[:,2] < 0).mean()*100, "%")
