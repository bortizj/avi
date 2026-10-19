# Automatic visual inspection
### Author: Benhur Ortiz-Jaramillo assisted by Claude [Opus 5.5]

Automatic visual inspection (AVI) is a technique for quality control in manufacturing. AVI has become a critical component in modern manufacturing and quality control processes [3, 4]. AVI uses cameras, lighting, and computational algorithms to check products without the need for a human inspector, enabling the detection of defects, the measurement of dimensions, and the verification of compliance with quality standards [1, 2]. AVI not only enhances product reliability and safety but also lowers operational costs and reduces human error [4, 5]. The scope of AVI spans various industries, including food processing, electronics, automotive, pharmaceuticals, textiles, additive manufacturing, and civil infrastructure, among others. Additionally, AVI is a key enabler of zero-defect manufacturing (ZDM), a quality strategy that aims to detect, repair, predict, and prevent defects so that no defective product leaves the factory [6]. Therefore, understanding AVI principles, applications, and benefits is essential for modern industrial automation applications.

Two related terms are used throughout this document, i.e., computer vision and machine vision. Computer vision is the scientific field that extracts information from images, while machine vision is the engineering discipline that applies computer vision, optics, and automation to industrial tasks [7, 8]. In this context, AVI is one of the main applications of machine vision.

The purpose of this document is to serve as reading material on how to design and architect AVI solutions. It is aimed at engineers and students with basic programming and mathematics skills, and no prior experience in computer vision is assumed. The document is organized as follows. First, we define manual and automatic visual inspection and show industrial examples of both. Next, we compare their strengths and weaknesses. Afterwards, we present a canonical seven-step AVI design process plus a supporting human-in-the-loop step, where each step is detailed with classical and modern techniques for 2D images and 3D point clouds. Finally, the document ends with real project examples, open problems, and best practices.

## Key terms used in this document

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

## Definitions and purpose

In this section we define manual (classical) and automatic visual inspection, each followed by a few industrial examples. The examples are paired, i.e., each automated example solves the same inspection task as one of the manual examples.

Please check out the detailed documentation here: 
[Definitions and purpose](definitions.md)

## Comparison between manual and automatic visual inspection

The table below summarizes the key differences between manual visual inspection performed by human operators and AVI systems across ten dimensions of performance, cost, and adaptability. The scores range from 0 (very poor) to 5 (excellent) and were estimated based on observations of past projects and expert judgment, supported where possible by the published studies cited in the table. Figure 10 shows a visual comparison of these scores as a radar (spider) chart, where each axis represents one dimension. The further a shape reaches along an axis, the better that approach performs on that dimension, highlighting the strengths and weaknesses of each approach.

| **Feature** | **Manual inspection (Human)** | **Score (0-5)** | **Automatic visual inspection (AVI)** | **Score (0-5)** |
| :--- | :--- | :---: | :--- | :---: |
| D1 \| Speed and throughput | Limited by human reaction time and physical endurance; creates bottlenecks on high-speed lines. | 1 | Very high throughput; capable of inspecting hundreds or thousands of parts per minute, e.g., 200 to 350 vials per minute [42]. | 5 |
| D2 \| Consistency and repeatability | Variable; quality assessment shifts from person to person and throughout a shift, e.g., ratings of the same bridge spanned up to five values [23]. | 2 | Highly consistent; applies the same rules every time, as long as lighting, optics, and products stay within the validated range. | 5 |
| D3 \| Objectivity and bias | Subjective; vulnerable to experience, mood, stress, and differing quality thresholds [30]. | 2 | Free of mood and fatigue; however, it still inherits the bias of its thresholds and training labels [35]. | 4 |
| D4 \| Fatigue and vigilance | Highly susceptible to fatigue and monotony; detection drops during long periods of watching [10, 33]. | 1 | Operates 24/7 without fatigue or loss of concentration. | 5 |
| D5 \| Cost structure | Low initial setup cost, but high ongoing operational labour costs and vulnerability to costly escapes. | 3 | High initial investment in hardware, software, and integration, but low cost per inspected unit. | 4 |
| D6 \| Adaptability to new defects | High flexibility; human inspectors easily reason through unexpected or novel defect types. | 5 | Limited flexibility; rule-based and supervised systems only detect known defects, while unsupervised anomaly detection can flag new deviations but cannot explain them [34]. | 2 |
| D7 \| Data and traceability | Often relies on manual record-keeping or paper checklists, making root-cause analysis difficult. | 1 | Logs every decision with images and metrics, providing real-time traceability. | 5 |
| D8 \| Detection performance | In one controlled study, inspectors caught about 85% of defects but rejected about 35% of good parts [5]; some studies suggest that error rates may reach 20 to 30% [46]. | 2 | High and measurable when well designed; supports precise metrology, e.g., about 50 µm in 3D [16]. | 4 |
| D9 \| Sensing range | Limited to visible light and human visual resolution; no direct 3D measurement. | 1 | Can use near-infrared, ultraviolet, X-ray, thermal, and 3D sensors beyond human vision [3]. | 5 |
| D10 \| Setup and changeover effort | Fast; inspectors can be trained in about two weeks [25] and switch products quickly. | 4 | Demanding; each new product requires optics design, data collection, labeling, integration, and validation. | 2 |

![spider-avi](assets/spider-avi.png)

*Figure 10. Radar chart of the scores in the table above.*

The comparison shows that both approaches have complementary strengths. AVI excels in speed, consistency, endurance, traceability, and sensing range, while humans excel in adaptability and fast changeover. For this reason, many industrial systems are hybrid [46], where AVI makes most of the decisions and humans review uncertain cases, investigate new defect types, and label data to improve the models. This human-centric view is also promoted by the Industry 5.0 strategy [47] and is the basis of steps (7) and (S) of the design process described below.

Additionally, a fair comparison requires measuring both approaches in the same way. Three metrics are commonly used, i.e., the detection rate (share of defective parts that are rejected), the escape rate (share of defective parts that are accepted), and the false reject rate (share of good parts that are rejected). These rates are measured using a test set of parts whose true condition is known. In attribute agreement analysis, each inspector or system classifies the test set several times, showing both accuracy and repeatability [48]. The pharmaceutical industry uses the same idea to qualify both human inspectors and machines [25, 27].

## Visual inspection design process

![design-process](assets/design-process.png)

*Figure 11. The AVI design process with seven main steps and one supporting step.*

The AVI process relies on a model that transforms physical manufacturing components into actionable quality decisions. This model is shown in Figure 11 and follows the processing chain found in standard machine vision references [3, 7, 8]. Before the lifecycle begins, the designer must define the requirements, e.g., the defect catalogue with limit samples, the tolerances, the required detection and false reject rates, the cycle time, and the interfaces to the production line [49]. Every later design choice is then checked against these requirements.

The lifecycle begins with (1) image capture, using cameras, lenses, and targeted illumination chosen to make defects clearly visible, to convert each part into digital images or 3D point clouds. Here, hardware triggers and strobe lighting synchronize the capture with the moving part. Next, (2) system calibration relates image measurements to the real world by correcting lens distortion, defining the pixel-to-millimeter mapping, and aligning cameras and lighting across stations. Calibration is done at commissioning and checked periodically using reference targets. Following acquisition, the digital data is (3) pre-processed to improve image quality before analysis through noise filtering, contrast normalization, and image alignment, or through outlier removal in the case of 3D point clouds.

Afterwards, (4) region of interest and object detection separate the target part or feature from its background, using classical methods such as template matching or deep learning methods such as segmentation networks. Thereafter, (5) feature extraction and anomaly detection modules find known defects and unknown anomalies, and measure dimensions, by combining rule-based algorithms with supervised and unsupervised machine learning. The resulting data is then (6) post-processed and fused across several views, sensors, or time steps, suppressing false alarms and issuing one definitive decision, i.e., Pass, Fail, or Review. Then, the (7) action and closed feedback loop phase executes the decision by sorting parts, logging data, and triggering alerts, e.g., through a PLC, while sending uncertain and rejected cases to human reviewers.

The process also includes a (S)upporting step named model sandbox. Here, human experts label new and difficult images, and these labels are used to retrain and validate the models offline, e.g., with active learning. Validated updates are then deployed back to steps (3) to (6), so the sandbox keeps the system improving after deployment. The table below summarizes the objective and typical industrial examples of each step.

| **Step** | **Objective** | **Industrial examples** |
| :--- | :--- | :--- |
| (1) Image capture | Acquire high signal-to-noise visual data. | Hardware triggers, strobe lighting, exposure time. |
| (2) System calibration | Normalize geometry, scale, and color. | Lens distortion correction, pixel-to-mm mapping. |
| (3) Image enhancement and pre-processing | Enhance contrast and remove noise. | Gaussian and bilateral filtering, histogram equalization. |
| (4) Region of interest and object detection | Isolate the target part or feature. | Template matching, pose estimation, segmentation. |
| (5) Feature extraction and anomaly detection | Detect flaws and measure dimensions. | Rule-based algorithms combined with deep-learning anomaly detection. |
| (6) Decision fusion and post-processing | Make a definitive Pass, Fail, or Review call. | Multi-view fusion, temporal filtering, false-alarm suppression. |
| (7) Action and closed feedback loop | Sort parts, log data, and trigger alerts. | PLC and digital I/O integration. |
| (S) Model sandbox | Improve and validate models with human input. | Active learning data pipeline. |

The process is iterative, since problems found in later steps often require changes to earlier ones. For example, a defect that is hard to detect is often solved with better lighting in step (1) rather than with a more complex algorithm in step (5) [3]. In the following sections, each step of the visual inspection design process is detailed, providing insights into the methodologies, tools, and considerations involved.

### (1) Image capture

Image capture is the step where the physical part becomes data, and its objective is to acquire visual data with a high signal-to-noise ratio, i.e., images or point clouds in which the defects of interest stand out clearly from the part, the background, and the sensor noise.

Please check out the detailed documentation here: 
[(1) Image capture](image_capture.md)

### (2) System calibration

System calibration is the step where the captured images are related to the real world, and its objective is to normalize geometry, scale, and color, i.e., to make sure that positions can be converted into millimeters and that gray values and colors mean the same on every camera, in every part of the image, and on every day.

Please check out the detailed documentation here:
[(2) System calibration](system_calibration.md)

### (3) Image enhancement and pre-processing

⚠️WARNING: Place holder for the pre-processing design process.⚠️

### (4) Region of interest and object detection

⚠️WARNING: Place holder for the object detection design process.⚠️

### (5) Feature extraction and anomaly detection 

⚠️WARNING: Place holder for the anomaly detection design process.⚠️

### (6) Decision fusion and post-processing 

⚠️WARNING: Place holder for the decision fusion design process.⚠️

### (7) Action and closed feedback loop

⚠️WARNING: Place holder for the feedback loop design process.⚠️

### (S) Model sandbox

⚠️WARNING: Place holder for the model sandbox design process.⚠️

## Past projects overview

⚠️WARNING: Place holder for the personal past projects overview design process.⚠️

## Conclusions, open problems, and best practices

This section summarizes the key findings, highlights open problems, and provides best practices for implementing an automated visual inspection system.

### Open problems

⚠️WARNING: Place holder for the open problems design process.⚠️

### Best practices

#### Image capture checklist

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

#### System calibration checklist

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

⚠️WARNING: Place holder for the best practices of steps (3) to (S).⚠️

### Conclusions

⚠️WARNING: Place holder for the conclusions design process.⚠️

## References

Please check out the detailed references here: 
[References](references.md)
