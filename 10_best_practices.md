# Best practices

⚠️ TODO: Clean, refine and complete the best practices section. This should be brief but comprehensive. ⚠️

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

## Feature extraction and anomaly detection checklist

The following table summarizes the design questions of step (5) together with typical industrial answers.

| **Design question** | **Typical industrial answer** |
| :--- | :--- |
| Which method checks each characteristic of the defect catalogue? | Dimensions with calibrated measurement, known critical defects with rules or supervised models, remaining appearance deviations with an anomaly detector; every defect type covered by at least one method [198]. |
| Is the characteristic a dimension? | Sub-pixel edges, calipers, and geometric fitting relative to the datums of the drawing, in calibrated images or point clouds [7, 187, 202]. |
| Is the measurement good enough for the tolerance? | Repeatability and bias measured on a certified reference part; resolution of at least one tenth of the tolerance; Gage R&R [48]. |
| What happens close to the tolerance limits? | Decision rule agreed with quality engineering, e.g., guard bands of the expanded uncertainty, with parts inside the guard band sent to Review [199, 203]. |
| Is the part appearance stable? | Golden template or variation model after sub-pixel alignment, trained on the full natural variation of good parts [137, 193]. |
| Does the surface have a texture? | Texture features, e.g., Fourier, Gabor, co-occurrence, or local binary patterns, with limits learned from good surfaces [135, 200, 205]. |
| Are there enough labeled defect images? | Supervised segmentation or detection networks, with weighted losses and few pixel-level labels where possible [174, 192, 201]. |
| Are defects rare or unknown? | Anomaly detection trained on good parts only, e.g., memory-bank, flow, or student-teacher methods [140, 194, 197]. |
| How is the threshold set? | On a separate set of many good images for the accepted false reject rate, checked on defective parts and limit samples for the required detection rate per defect type. |
| How are methods compared and validated? | AUROC and PRO for model selection [209, 215]; detection, escape, and false reject rates at the operating threshold on real parts for release [48]. |
| Are small defects preserved? | Tiling at full resolution instead of downsizing; identical pre-processing in training and production [140, 141, 142]. |
| Can the result be explained? | Defect position, size, and score stored with each result; anomaly maps, masks, or Grad-CAM shown for Review cases [223]. |
| How is a 3D part compared with its CAD model? | Registration with ICP from the pose of step (4), signed point-to-surface distances, visibility by ray casting, and clustering of out-of-tolerance regions [149, 185, 195]. |
| Which alignment does the CAD comparison use? | The datum system of the drawing for conformity decisions; best fit only to judge shape; local features measured as separate dimensions [202, 227]. |
| Are the features used beyond the decision? | Measurements and scores logged per part for statistical process control, drift monitoring, and the sandbox (S) [196]. |
| Are models and thresholds traceable? | Model, threshold, calibration, and pre-processing versions stored with every result; revalidation after changes of product, supplier, or lighting [110]. |

## Decision fusion and post-processing checklist

The following table summarizes the design questions of step (6) together with typical industrial answers.

| **Design question** | **Typical industrial answer** |
| :--- | :--- |
| Which decisions does the system make? | Pass, Fail with a reason code, and Review; grades or repair instructions where needed; an invalid result is never a Pass. |
| What do escapes, false rejects, and reviews cost? | Costs agreed with production and quality engineering; reject when the calibrated probability exceeds $C_{\text{fr}} / (C_{\text{fr}} + C_{\text{esc}})$ [231]. |
| Are the scores probabilities? | Calibrated on a validation set with Platt scaling, isotonic regression, or temperature scaling; checked again when the process or the defect prevalence changes [232, 233, 234]. |
| Which parts go to Review? | Parts between two cost-based thresholds, measurements inside guard bands, and anomalies without a known defect type [199, 235]; Review rate within the capacity of the reviewers. |
| How is the defect catalogue applied? | Decision table per defect type, zone, severity, and count, e.g., critical, major, and minor defects [18, 25, 28]; the most severe finding becomes the reason code. |
| Are defects counted only once? | Defects merged in part coordinates across tiles and views before size and count limits are applied. |
| How are several views combined? | Evidence fused per location in part coordinates, with the overlap of the views planned in step (1) [239]; OR rules only with a false reject budget per source, since $1-(1-\alpha)^n$ grows with every source. |
| How are sensors and algorithms combined? | 2D and 3D results fused in part coordinates [229, 230]; findings of the anomaly detector alone go to Review; the first stage of a cascade is set for a very high detection rate. |
| How are image sequences used? | Static background removed with a temporal median; detections confirmed by persistence over M of N frames and by tracking [241, 242]; motion rules validated with real test units. |
| How are false alarms suppressed? | ROI and zone masks, size and contrast filters, consistency across views and frames, and verification of candidates [243, 244]; every rule checked on known defective parts; suppressed candidates logged. |
| How is the Review station designed? | Images of all views, defect location and size, explanation maps, and reason code [223]; known test parts mixed into the queue to monitor reviewers and automation bias [245]; decisions stored as labels for the sandbox (S). |
| What happens when no decision can be made? | Fail-safe logic: missing image, missed trigger, part not found, invalid measurement, or timeout lead to Fail or Review with an alarm. |
| Is the decision available in time? | Worst-case latency measured; decision ready before the part reaches the reject station of step (7). |
| How is the decision validated? | Detection, escape, false reject, and Review rates per part and per defect type; 95% upper bound of the escape rate, e.g., 299 defective parts without escape for less than 1% [246, 247]; repeated inspections with accept, gray, and reject zones [248, 249]. |
| How is the decision verified in production? | Golden parts, sampling of accepted parts, e.g., AQL 0.65% for injectable drugs [11, 26], and control charts of the reject and Review rates [196]. |
| Is the decision logic traceable? | Decision table, thresholds, and suppression rules versioned with models and calibration; reason code, evidence, and versions logged with every decision [110]. |

## Action and closed feedback loop checklist

The following table summarizes the design questions of step (7) together with typical industrial answers.

| **Design question** | **Typical industrial answer** |
| :--- | :--- |
| Which actions does the system take? | Reject, sort or grade, mark, repair instruction, Review, hold or stop, alert, log, and feedback to the process and the inspection; each with a defined owner. |
| Who controls the actuator? | The PLC, programmed according to IEC 61131-3, fires the reject and stops the line; the vision system delivers decisions and data [250, 251]. |
| How are vision system and PLC connected? | Digital I/O handshake with trigger, Ready, Busy, Result Valid, result bits, Error, and heartbeat; fieldbus or OPC UA for data, preferably with the machine vision information model [252, 253]. |
| Is every result bound to its part? | Part counter or identifier returned with each result; exactly one result per trigger checked by the PLC; alarm on missed or double triggers. |
| Is the decision available in time? | Latency budget $t_{\text{lat}} \le d/v - t_{\text{act}} - t_{\text{margin}}$, measured at maximum line speed and full load, including queueing and rare long delays (Figure 35). |
| How is the part tracked to the actuator? | Encoder-based tracking with a FIFO queue or shift register instead of a fixed time delay [258]; distance and encoder checked after maintenance. |
| Is the reject fail-safe? | Positive release, i.e., only an explicit and valid Pass is accepted; reject confirmation, bin-full, bin-lock, and air-pressure monitoring; faults reset only by authorized staff [259]. |
| Is the whole chain tested? | Test parts that must be rejected, e.g., at every shift start, through camera, decision, tracking, actuator, and confirmation. |
| What is logged for each part? | Part identity, time, lot, decision, reason code, measurements, scores, defect lists, station, and versions of recipe, models, thresholds, and calibration [110]. |
| Are the clocks synchronized? | Precision Time Protocol or equivalent between vision system, PLC, and MES [260]. |
| Which images are stored? | All Fail and Review images without lossy compression, a random sample of Pass images, and all measurements; retention defined by industry and customer. |
| Are records protected? | Audit trails and data integrity according to ISO 9001 and, in regulated industries, 21 CFR Part 11 and the ALCOA+ principles [110, 262, 263]. |
| Which alerts exist and who responds? | Health, quality, and trend alerts with defined cause, response, and priority; stop or hold when the inspection cannot be trusted [264]. |
| Can operators handle the alarm rate? | Long-term average below about 12 alarms per hour and no floods of more than 10 alarms in 10 minutes; alarms grouped, with hysteresis, and the alarm rate monitored [265, 266]. |
| How are process changes detected? | EWMA or CUSUM charts on measurements and scores, with limits from a stable period and false alarms counted in hours of production [196, 267]. |
| Is the process adjusted automatically? | Run-to-run or integral control with a low gain that respects dead time and noise; no adjustment by single results (tampering); limits and logging of every adjustment [268, 269, 270]. |
| Are results passed forward? | Grades, defect positions, and measurements sent to sorting, repair, or mating steps, e.g., with IPC-CFX in electronics [31, 255, 271]. |
| Where do new labels come from? | Review decisions, re-inspection of rejects, complaints, and a random audit of accepted parts sized for the escape rate to be found [272]. |
| Is the inspection system monitored? | Inputs (brightness, sharpness, golden part), outputs (score distributions, measurements), and outcomes (reject, Review, and audit results) with control charts and defined responses [274, 275, 276]. |
| How are models and calibrations updated? | Validation in the sandbox (S), shadow mode, versioned deployment with rollback, and change control; static models in regulated, critical applications [110, 276, 277]. |
| How is 3D feedback used? | Metrology reports in QIF, tool offsets and build compensation from deviation maps, and repair paths from defect positions [16, 31, 261, 278]. |

## Model sandbox checklist

The following table summarizes the design questions of step (S) together with typical industrial answers.

| **Design question** | **Typical industrial answer** |
| :--- | :--- |
| Which annotation type does each problem need? | The cheapest type that supports steps (4) to (6), i.e., image-level labels for presence, boxes or points for position and count, masks or measured attributes for size limits; the richest level for test sets and critical defect types. |
| Can the annotation effort be reduced? | Review decisions stored as labels; weak or mixed supervision with few masks [201]; model-assisted pre-labels that humans correct [177, 178]. |
| Is there an annotation guideline? | Derived from the defect catalogue with limit samples; classes, look-alike classes, label geometry, and an uncertain option; versioned with the datasets [25]. |
| Are the labels consistent? | Golden set for every annotator; double labeling with adjudication of a share of the images; Cohen's kappa above about 0.75 and IoU tracked per annotator [48, 285, 286]. |
| Do the labels follow the defect catalogue? | Checked against expert labels and limit samples, since agreement does not reveal a bias that all annotators share (Figure 39). |
| How are label errors found? | Likely errors ranked by the disagreement between labels and out-of-sample predictions and reviewed by humans [287]; test labels never corrected automatically by the model. |
| Which images are labeled? | Review cases, uncertainty and diversity with a random share in every batch [288, 292]; new products, suppliers, and conditions first. |
| How are unknown defect types found? | Random share of the labeling batches and the audit of accepted parts of step (7) [272] (Figure 40). |
| Is the human feedback used beyond retraining? | Review and audit results analyzed by reason code, position, size, and time; changes of capture, calibration, pre-processing, or decision logic where they are more effective. |
| How are unlabeled and synthetic data used? | Pseudo-labels, pasted defects, and rendered CAD data for training only [224, 294, 295]; validation on real images with expert labels. |
| How are the datasets split? | By part, lot, and time; protected test set with verified labels, never used for development [277, 299]. |
| Is the test set reused for tuning? | No; it accepts or rejects finished candidates [300], while a challenge set of limit samples, past escapes, and past false rejects checks for regressions. |
| Are datasets and models documented? | Datasheets and model cards with source, guideline, intended use, known limitations, and performance per defect type [298, 301]. |
| How is a model retrained? | On the complete versioned dataset, not only on new data, to keep known defect types [302]; static models in critical applications [277]. |
| How is a candidate released? | Offline replay of steps (3) to (6), part-level rates per defect type with confidence bounds [246, 247], comparison with production, shadow mode, versioned deployment, and rollback [276, 277]. |
| How are 3D data labeled? | Labels on height maps or calibrated 2D images transferred to the points, regions defined on the CAD model, simulated scans for training, and real scans for validation [185, 228]. |
