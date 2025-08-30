# Lidar_processing
Assignment 5

# Task 1 — Ground Level Estimation

### Method
The point cloud files have x, y, z values.  
I only look at the z values (height). To find the ground level:

1. I remove very high and very low outliers.  
2. I make a histogram of the z values with `np.histogram`.  
3. I check where the biggest peak is in the lower part of the histogram.  
4. That peak is the ground level.  

I wrote this in the function `get_ground_level()`.

### Results
- dataset1 ground level: **61.269**
- dataset2 ground level: **61.255**

Both datasets give almost the same ground level (around 61.2).  
The higher parts in the histograms must be other things like rails, pylons, or trees. 

### Histograms
Here are the histograms with a red dashed line showing the ground level:

![dataset1 histogram](plots/dataset1_hist.png)  
![dataset2 histogram](plots/dataset2_hist.png) 

