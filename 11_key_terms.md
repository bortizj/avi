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
