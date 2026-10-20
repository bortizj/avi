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
| Pass / Fail / Review | Decision classes of step (6), where Review sends a part with inconclusive evidence to a human inspector. |
| Reason code | Rule, defect, or measurement that caused a Fail or Review decision, stored with the decision. |
| Fail-safe decision | Design rule by which missing, invalid, or late results lead to Fail or Review, never to Pass. |
| Score calibration | Mapping of model scores to probabilities that match the observed frequency of defects, e.g., Platt scaling or temperature scaling [232, 233]. |
| Reject option | Option of a classifier to withhold a decision when the evidence is ambiguous; the basis of the Review class [235]. |
| Conformal prediction | Method that turns model scores into sets of plausible classes with a guaranteed coverage probability [237]. |
| Data-, feature-, and decision-level fusion | Combination of sources before the analysis (early fusion), of their features, or of their scores and decisions (late fusion) [238]. |
| Sum rule / majority vote | Decision-level fusion that adds the scores / counts the decisions of several sources [239]. |
| M-of-N detection | Confirmation of a detection only when it occurs in at least M of N consecutive frames or observations [241]. |
| Tracking / Kalman filter | Linking of detections across frames into object tracks / recursive estimator that predicts the next position of a moving object [242]. |
| False call | Defect reported by an inspection system that a review finds acceptable; common term in AOI [243]. |
| Automation bias | Tendency of humans to follow the suggestion of an automated system even when the evidence contradicts it [245]. |
| Clopper-Pearson bound / rule of three | Exact confidence bound of a binomial rate / approximation 3/n of the 95% upper bound when no event occurs in n trials [246, 247]. |
| Probability of rejection (Knapp method) | Share of repeated inspections that reject a test unit; it sorts units into accept, gray, and reject zones [248, 249]. |
| Acceptance quality limit (AQL) | Worst tolerable quality level of a process in acceptance sampling, e.g., 0.65% for the batch release of injectable drugs [11, 26]. |
| EWMA | Exponentially weighted moving average, a control chart that detects small, slow drifts of a process [196]. |
| ISA-95 automation levels | Layers of a plant from sensors and actuators through the PLC to MES and ERP, standardized as IEC 62264 [250]. |
| Digital I/O handshake | Exchange of trigger, status, and result signals between a vision system and a PLC, e.g., Ready, Busy, Result Valid, and Error. |
| Heartbeat | Signal that toggles at a fixed rate while a system is alive, so that a frozen system is detected within a known time. |
| OPC UA / OPC 40100 | Vendor-independent industrial communication standard (IEC 62541) / its companion specification for machine vision systems [252, 253]. |
| Part tracking (shift register, FIFO) | Queue in the PLC that follows each part and its result from the camera to the actuator. |
| Encoder-based tracking | Tracking of the part position by counting encoder pulses of the conveyor instead of measuring time. |
| Positive release | Rule by which a part is only accepted with an explicit and valid Pass decision; everything else is rejected. |
| Reject confirmation | Sensor check that a rejected part has actually left the line, e.g., entered the reject bin [259]. |
| Audit trail | Secure, time-stamped record of the creation, modification, and deletion of records [262]. |
| ALCOA+ | Data integrity principles: attributable, legible, contemporaneous, original, accurate, complete, consistent, enduring, and available [263]. |
| Jidoka / andon | Principle of stopping automatically at an abnormality / signal that calls for help [264]. |
| Alarm flood | More alarms than an operator can handle, e.g., more than 10 new alarms within 10 minutes [266]. |
| Statistical process control (SPC) | Use of control charts to separate the natural variation of a process from changes with an assignable cause [196]. |
| Run-to-run control | Feedback control that adjusts the process settings of the next run or part from the measurements of previous ones [268]. |
| Tampering | Adjusting a stable process by every single deviation, which increases its variation [269]. |
| Dead time | Delay between a change of the process and its first effect on the inspection result. |
| Feed-forward | Use of inspection results to guide a later process step, e.g., repair or sorting. |
| Selective labels | Situation where outcomes are only observed for the cases selected by the current decision, e.g., only rejected parts are reviewed [272]. |
| Audit sample | Random sample of accepted parts reviewed by humans to find escapes. |
| Concept drift / dataset shift | Change of the data or of the relation between data and correct decisions after a model was trained [274]. |
| Shadow mode | Operation of a new model version in parallel with the current one, without acting on the parts. |
| Static / dynamic model | Model whose parameters are fixed during use / that keeps adapting during use [277]. |
| Precision Time Protocol (PTP) | Network protocol that synchronizes the clocks of devices, standardized as IEEE 1588 [260]. |
