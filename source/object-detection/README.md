# Figure scripts for section (4) Region of interest and object detection

These scripts generate Figures 23 to 26 of `05_object_detection.md`. All scenes are simulated, so no input data is needed, and every script uses a fixed random seed, so it reproduces the figure and the numbers quoted in the text.

| **Script** | **Figure** | **Output** |
| :--- | :--- | :--- |
| `fig23_roi_classical_2d.py` | Figure 23, classical 2D detection (threshold, blobs, watershed, Hough circles) | `roi-classical-2d.png` |
| `fig24_roi_template_matching.py` | Figure 24, NCC versus shape-based matching | `roi-template-matching.png` |
| `fig25_roi_learned_segmentation.py` | Figure 25, Otsu threshold versus a learned pixel classifier, and domain shift | `roi-learned-segmentation.png` |
| `fig26_roi_pointcloud_segmentation.py` | Figure 26, RANSAC plane fit and DBSCAN clustering of a point cloud | `roi-pointcloud-segmentation.png` |

`style.py` holds the shared plot style and must stay in the same folder as the scripts.

## Usage

```bash
pip install -r requirements.txt
python fig23_roi_classical_2d.py
python fig24_roi_template_matching.py
python fig25_roi_learned_segmentation.py
python fig26_roi_pointcloud_segmentation.py
```

Each script writes its PNG to the current folder and prints the values used in the text, e.g., the number of blobs, the matching scores, the IoU values, and the number of clusters per eps. The published figures were generated with Python 3, NumPy 2.x, OpenCV 4.x, SciPy, scikit-learn, scikit-image, and Matplotlib; other versions may change the last digit of some printed values.

## Notes

- The figures use the Inter font when it is installed; otherwise Matplotlib falls back to DejaVu Sans, which changes only the typography.
- Figure 24 searches all rotations in steps of 2° and takes about a minute on a laptop CPU.
- Figure 25 trains a random forest on 25 images and evaluates 80 test images; it takes one to two minutes.
