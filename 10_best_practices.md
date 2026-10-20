# Best practices

## Image capture checklist

The following table summarizes the design questions of step (1) together with typical industrial answers.

| **Design question** | **Typical industrial answer** |
| :--- | :--- |
| What makes the defect physically different? | Color, gloss, shape, transparency, moisture, chemistry, temperature, or density; this decides the illumination and the band. |
| How many pixels cover the smallest defect? | About 3 (2 to 4) pixels per smallest defect; this sets the sensor resolution for the given FOV [50, 51]. |
| Which illumination geometry gives contrast? | Bright field, dark field, backlight, coaxial, dome, or structured light; test with real good and defective samples [53, 54]. |
| Which wavelength band? | Visible with monochromatic LED by default; UV, NIR, SWIR, thermal, or X-ray when the defect requires it (Figure 13). |
| Standard or telecentric lens? | Telecentric for precise dimensional measurement; standard for detection [75]. |
| Area-scan or line-scan camera? | Area scan for discrete parts; line scan with encoder for webs, large parts, and cylinders [78, 79]. |
| How short must the exposure be? | $t_{\text{exp}} \le b \cdot s / v$, typically with strobe and overdriven LEDs on fast lines [83, 85]. |
| How is the capture synchronized? | Hardware trigger from a part sensor or encoder to the camera and the light controller [85]. |
| How is ambient light excluded? | Enclosure, band-pass filter matched to the LED, and bright strobes [76]. |
| Is 2D enough, or is 3D needed? | 3D when heights, volumes, or CAD deviations matter; laser triangulation or structured light for precision [56, 57]. |
| How is the camera chosen and verified? | EMVA 1288 data for 2D cameras [81]; VDI/VDE 2634 tests for optical 3D systems [90]. |

## System calibration checklist

The following table summarizes the design questions of step (2) together with typical industrial answers.

| **Design question** | **Typical industrial answer** |
| :--- | :--- |
| Which quantities does the system report? | Positions and dimensions need geometric calibration and a pixel-to-mm mapping; fixed gray-value thresholds need flat-field correction; color decisions need color calibration. |
| Is the camera model fitted correctly? | Planar target at the working distance with fixed focus and aperture, covering the whole FOV and tilted by about 30 to 45°, with at least 10 to 15 views; low RMS reprojection error [94, 95]. |
| Is the reference traceable? | Certified glass or ceramic target, gauge blocks, or golden parts with certificates; calibration records are kept [96, 110]. |
| Is a single mm/px factor enough? | Only after distortion correction, for a plane perpendicular to the optical axis at a fixed distance; otherwise a homography, a telecentric lens, or 3D measurement [74, 93]. |
| Is the measurement capable? | Gage R&R with %GRR below 10% (10 to 30% conditionally); resolution of at least one tenth of the tolerance [48]. |
| Are the camera settings fixed? | Auto-exposure, auto-gain, and auto white balance off; trigger delay, strobe inside the exposure, motion blur, and trigger-to-image counts checked at line speed [83]. |
| Are line-scan pixels square? | Encoder step equal to the pixel size across the line; scale in the direction of motion calibrated with markers at a known distance [97]. |
| Is the image uniform and stable? | Dark-frame and flat-field correction [98]; constant-current lights, warm-up, and a monitored reference patch [113]. |
| Are colors comparable between cameras and days? | Fixed white balance and a color correction matrix fitted to a reference chart; ΔE00 tolerance agreed per product [99, 101]. |
| Are all sensors in one coordinate system? | Common calibration target for multiple cameras, hand-eye calibration for robots, and an encoder-to-image mapping for conveyors [95, 117]. |
| Is the 3D sensor verified? | Factory intrinsic calibration plus user extrinsic calibration [103]; acceptance and reverification tests according to ISO 10360-13 [104]. |
| When is the system recalibrated? | Verification at every shift with a golden part or reference target; full recalibration after any change of the optical chain, a collision, or a failed verification [95, 110]. |

## Image enhancement and pre-processing checklist

The following table summarizes the design questions of step (3) together with typical industrial answers.

| **Design question** | **Typical industrial answer** |
| :--- | :--- |
| Which nuisance does each operation remove? | One documented nuisance per operation, e.g., noise, defective pixels, shading, texture, or misalignment; no operation without a measured benefit. |
| Can the problem be solved in step (1) instead? | More light, a longer exposure within the motion-blur limit, or a better illumination geometry before strong filters [3]. |
| Is the data lossless and linear? | 10-bit or 12-bit data, camera gamma and automatic functions off, no lossy compression for analysis or labeling [81, 95]. |
| In which order are the operations applied? | Defect pixel correction, dark and flat-field correction, demosaicing and color conversion, denoising, geometric correction, background and contrast, alignment, deep-learning formatting. |
| How is random noise reduced? | Frame averaging when the part is static (noise divided by $\sqrt{N}$); otherwise a Gaussian, median, or edge-preserving filter clearly smaller than the smallest defect [119]. |
| How are defective pixels handled? | Defect pixel correction in the camera, with a defect map measured at operating temperature [122, 121]. |
| Does a filter remove defects? | Method noise and defect CNR checked on images with known defects of every type [128]. |
| How is uneven shading removed? | Flat-field correction for the shading of the system (step (2)); per-image background division or top-hat, with a kernel larger than the largest defect, for the shading of the part [134]. |
| Are image-dependent mappings combined with fixed thresholds? | No; histogram equalization and CLAHE for human review or learned inputs, fixed look-up tables for rule-based decisions [133]. |
| How are periodic textures handled? | Fourier notch filtering with excluded or windowed borders, or texture features in step (5) [135]. |
| Is alignment needed? | Sub-pixel registration, e.g., phase correlation or ECC, before every golden-template comparison [138, 139]. |
| How are images prepared for deep learning? | The same code and parameters in training and production; tiling instead of downsizing when defects are small [142, 141]. |
| How are point clouds cleaned? | Crop box, statistical outlier removal, voxel grid, and a surface-aware filter, each with a scale below the smallest defect [146, 148]. |
| Does the chain fit the cycle time? | Separable and running-sum filters, processing of regions of interest only, in-camera correction, and GPU processing for heavy filters. |
| How is the chain validated and traced? | Detection, escape, and false reject rates on a test set with and without each operation; parameters versioned with the calibration data [48, 110]. |

## Region of interest and object detection checklist

The following table summarizes the design questions of step (4) together with typical industrial answers.

| **Design question** | **Typical industrial answer** |
| :--- | :--- |
| Which output do the later steps need? | The simplest output that supports steps (5) and (6), i.e., presence, box, oriented box or 2D pose, mask, keypoints, or 6D pose. |
| Can detection be avoided or simplified? | Fixtures, nests, singulation, guide rails, backlight, or a contrasting background before complex algorithms [3]. |
| How accurate must the localization be? | Derived from the ROI margin, the smallest defect, and the measurement tolerance; sub-pixel for fixtured measurements [152]. |
| Is the object detectable under all expected conditions? | Tested early on real images of good, defective, and borderline parts at the worst positions and appearances. |
| High contrast and separated parts? | Fixed or Otsu threshold with blob analysis and feature filters [160, 166]. |
| Touching parts? | Distance transform and watershed for compact parts [156]; instance segmentation or region growing otherwise [157, 182]. |
| Simple geometric features? | Canny edges with Hough transform or RANSAC fitting, with the search range limited to the expected sizes [161, 167, 162]. |
| Rigid part in a random pose? | Shape-based matching over the full range of rotations, with image pyramids and a documented minimum score [7, 152]. |
| Variable appearance or cluttered background? | Detection or segmentation networks trained on labeled images covering all products, backgrounds, and lighting conditions [155, 163]. |
| How is the detector evaluated? | Recall of parts, false detections per image, localization error in pixels, millimeters, and degrees, and worst-case time on a separate test set; AP for model comparison [180]. |
| What if no part, too many parts, or a low-score part is found? | An explicit Fail or Review rule in step (6); never a Pass. |
| Will a learned detector meet new conditions? | New backgrounds, products, suppliers, and lights treated as changes that need new labeled validation data in the sandbox (S). |
| How is the conveyor or table removed in 3D? | RANSAC plane fit with a distance threshold above the sensor noise and below the lowest feature [162, 164]. |
| How are 3D objects separated? | DBSCAN or Euclidean clustering with eps above the point spacing and below the smallest gap; normal-based region growing for touching parts [165, 182]. |
| How is the 6D pose found for CAD comparison? | Point pair features or a learned pose estimator for the initial pose, ICP for refinement, and ray casting for the visible region [149, 158, 159, 185]. |
| Are detection results traceable and monitored? | Detector version stored with each result; match scores logged and trended to detect drift [110]. |

⚠️WARNING: Place holder for the best practices of steps (5) to (S).⚠️
