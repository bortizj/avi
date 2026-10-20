# Key terminology

| **Term** | **Meaning** |
| :--- | :--- |
| Machine vision | Engineering use of cameras, optics, and computer vision to solve industrial tasks [7]. |
| Escape (false negative) | Defective part that the inspection accepts. |
| False reject (false positive) | Good part that the inspection rejects. |
| Zero-defect manufacturing (ZDM) | Strategy to detect, repair, predict, and prevent defects [6]. |
| CAD model | Computer-aided design file holding the nominal (ideal) geometry of a part. |
| Point cloud | Set of 3D points sampling the surface of an object, typically produced by 3D scanners or LiDAR. |
| Deflectometry | Measurement of a glossy surface by observing how it reflects a known light pattern. |
| SLAM | Simultaneous localization and mapping, i.e., a robot builds a map while it locates itself in that map. |
| PLC | Programmable logic controller, i.e., the industrial computer that controls machines on the line. |
| MES / ERP | Manufacturing execution system / enterprise resource planning, i.e., software that tracks production and business data. |
| Human-in-the-loop | Design in which humans review machine decisions and feed corrections back into the system. |
| Cycle (takt) time | Time available to process one part. |
| Intrinsic parameters | Camera parameters that describe the camera itself, i.e., the focal length, the principal point, and the lens distortion. |
| Extrinsic parameters | Rotation and translation that describe the pose of a camera relative to a world, robot, or other camera coordinate system. |
| Reprojection error | Distance between the detected calibration points and the points predicted by the calibrated camera model. |
| Flat-field correction | Pixel-wise correction with dark and flat reference images that removes sensor non-uniformity, vignetting, and uneven illumination. |
| Golden part | Reference part with known dimensions and known defects, used to verify an inspection system. |
| Gage R&R | Gauge repeatability and reproducibility study that measures how much of the tolerance is consumed by the measurement system [48]. |
| Contrast-to-noise ratio (CNR) | Contrast of a defect against its surroundings divided by the standard deviation of the noise. |
| Point operation | Gray-value mapping applied to each pixel independently of its neighbors, e.g., a look-up table or a gamma mapping. |
| Spatial filter | Operation that computes each output pixel from a neighborhood of input pixels, e.g., a Gaussian or median filter. |
| Edge-preserving filter | Smoothing filter that averages less across edges, e.g., the bilateral filter, the guided filter, or anisotropic diffusion. |
| Histogram equalization / CLAHE | Image-dependent mapping that spreads the gray values evenly; CLAHE does so locally and limits the contrast gain with a clip limit. |
| Top-hat transform | Morphological operation that keeps bright (white top-hat) or dark (black top-hat) structures smaller than a structuring element. |
| Notch filter | Frequency-domain filter that removes selected frequency peaks, e.g., those of a periodic texture. |
| Golden template | Image of a known good part that serves as the reference in an image comparison. |
| Image registration | Estimation of the transformation that aligns an image with a reference image or model. |
| Method noise | Difference between an image and its filtered version, used to check what a filter removes [128]. |
| Training-serving skew | Difference between the data processing during model training and during operation [142]. |
| Statistical outlier removal | Removal of 3D points whose mean distance to their nearest neighbors is unusually large [146]. |
| Voxel grid | 3D grid of small cubes in which all points of each cube are replaced by their centroid. |
| Flying pixels | Spurious 3D points between foreground and background at depth edges, typical of time-of-flight cameras [143]. |
| Region of interest (ROI) | Part of an image or point cloud that is passed on for analysis, e.g., a rectangle around a component or the mask of a part. |
| Fixturing | Definition of inspection ROIs in the coordinate system of the part, so that they move with the position and rotation found by the detection [152]. |
| Bounding box / oriented bounding box | Axis-aligned rectangle around an object / rectangle that also follows the rotation of the object. |
| Semantic / instance segmentation | Assignment of a class / of an individual object to every pixel or point. |
| Blob analysis | Grouping of thresholded pixels into connected regions and computing their features, e.g., area, center, and orientation. |
| Watershed transform | Segmentation that floods an image from markers; used with the distance transform to separate touching objects [156]. |
| Hough transform | Voting method that finds lines, circles, or other shapes from edge points [167, 169]. |
| RANSAC | Robust fitting that repeatedly fits a model to random minimal samples and keeps the model with the most inliers [162]. |
| Normalized cross-correlation (NCC) | Similarity measure between a template and an image window that is invariant to linear brightness and contrast changes [170]. |
| Shape-based matching | Template matching that compares edge directions instead of gray values, robust to occlusion, clutter, and illumination changes [152]. |
| Non-maximum suppression (NMS) | Removal of overlapping duplicate detections of the same object, keeping the one with the highest score. |
| Intersection over union (IoU) | Area of the intersection of a predicted and a true region divided by the area of their union. |
| Average precision (AP) / mAP | Summary of the precision-recall curve of a detector; mAP is the mean of the AP over all classes [179, 180]. |
| 6D pose | Position and orientation of an object in space, i.e., three translations and three rotations. |
| DBSCAN | Density-based clustering with a radius eps and a minimum number of points, which also labels isolated points as noise [165]. |
| Point pair features | Model-based 3D detection that votes for the object pose using the distances and normal angles of point pairs [158]. |
| Ray casting | Tracing rays from a sensor into a 3D model to compute the visible surfaces or a virtual scan [185]. |
| Domain shift | Difference between the conditions of the training data and of operation, e.g., a new background, which can degrade a learned model. |
| Caliper | One-dimensional edge measurement along a line perpendicular to an expected edge, averaged over several parallel lines [7]. |
| Sub-pixel accuracy | Localization of an edge or feature more precisely than one pixel, e.g., by interpolating the gradient profile [187]. |
| Guard band | Margin inside a tolerance limit that reduces the risk of accepting a nonconforming part at the cost of rejecting more conforming parts [199]. |
| Consumer's / producer's risk | Probability of accepting a nonconforming item / of rejecting a conforming item [199]. |
| Variation model | Golden-template comparison that learns a mean and a variation image from good parts and allows larger differences where good parts vary more [193]. |
| Texture features | Statistics of the local gray-value pattern, e.g., co-occurrence features, local binary patterns, or Gabor filter responses [205, 206, 207]. |
| Anomaly detection | Detection of deviations from a model of good parts, trained without defect images [197]. |
| Anomaly score / anomaly map | Measure of how much an image / each pixel deviates from good parts. |
| Memory bank | Stored features of good image patches; a new patch is scored by the distance to its nearest neighbor in the bank [140]. |
| Structural / logical anomaly | Local physical flaw, e.g., a scratch / violation of a constraint of the whole scene, e.g., a missing or misplaced component [218]. |
| AUROC / PRO | Area under the ROC curve, which measures how well scores rank defects above good parts / per-region overlap, which weights each defect region equally [215]. |
| Deviation map (heat map) | Color-coded signed distance of every measured point from the CAD model. |
| Best-fit / datum alignment | Registration that minimizes all deviations / that places the part on the datums defined by the drawing [227]. |
