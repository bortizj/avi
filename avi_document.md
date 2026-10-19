# Automatic visual inspection
### Author: Benhur Ortiz-Jaramillo

Automatic visual inspection (AVI) is the use of cameras, lighting, and algorithms to check products without a human inspector [1, 2]. AVI detects defects, measures dimensions, and verifies that products meet quality standards. It is a core technology of modern manufacturing and quality control [3, 4].

AVI improves product reliability and safety. It also lowers operating costs and reduces human error [4, 5]. Its use spans many industries. Examples are food processing, electronics, automotive, pharmaceuticals, textiles, additive manufacturing, and civil infrastructure. AVI is also a key enabler of zero-defect manufacturing (ZDM). ZDM is a quality strategy that aims to detect, repair, predict, and prevent defects so that no defective product leaves the factory [6].

Two related terms appear throughout this document. Computer vision is the scientific field that extracts information from images. Machine vision is the engineering discipline that applies computer vision, optics, and automation to industrial tasks [7, 8]. AVI is one of the main applications of machine vision.

This document is the reading material for a course on how to design and architect AVI solutions. It targets engineers and students with basic programming and mathematics skills. No prior experience in computer vision is assumed. The document is organized as follows. First, it defines manual and automatic visual inspection and shows industrial examples of both. Second, it compares their strengths and weaknesses. Third, it presents a canonical seven-step AVI design process plus a supporting human-in-the-loop step. Each step is then detailed with classical and modern techniques for 2D images and 3D point clouds. The document ends with real project examples, open problems, and best practices.

## Definitions and purpose

This section defines manual (classical) and automatic visual inspection. Each definition is followed by industrial examples. The examples are paired. Each automated example solves the same inspection task as one manual example. The pairing makes the differences between both approaches easy to see.

### Classical visual inspection

![human-inspector](assets/human-inspector.png)

*Figure 1. The human inspector as an inspection system. The eye senses, the brain decides, and the hands act.*

Before defining AVI, we must understand manual inspection. Manual inspection is also called classical or human visual inspection. It is the examination of products, components, or structures with the human eye to find flaws, defects, or non-compliance with quality standards [9, 10]. Inspectors often use aids such as controlled lighting, magnifiers, gauges, or simple hand tools.

Figure 1 shows the human inspector as a three-part system. The eye captures the visual information. The brain compares what it sees with a mental model of a good part. The hands act on the decision, for example by removing a part from the line. The lower panel shows a simplified quality inspection space. Each dot is one product, described by the visual features the inspector perceives. Each color is one quality class. The classes overlap. This overlap is one reason why decisions vary between inspectors and over time [5].

Manual inspection is done in two ways. In 100% inspection, every unit is checked. In sampling inspection, only a random sample of each lot is checked. The whole lot is then accepted or rejected based on the sample, for example with the plans of ISO 2859-1 [11]. Typical manual inspection tasks are described below.

#### Food and egg inspection and sorting

![eggs-inspection](assets/eggs-inspection.png)

*Figure 2. Manual egg grading on a conveyor. Typical defects: rough shells, blood spots, and soft shells. Image generated with Gemini AI.*

Quality-control sorters stand beside moving conveyor belts. They inspect raw or semi-processed farm products, such as eggs, fresh fruit, root vegetables, nuts, and bakery items. They remove bruised, rotten, or misshapen items. They also remove foreign material, such as stones, stems, dirt clumps, or field debris [12]. In egg grading, inspectors check the shell for cracks, dirt, rough texture, and soft or thin shells [13]. Internal defects, such as blood spots, are invisible under normal light. Inspectors find them by candling. Candling means holding the egg against a bright light in a dark room and rotating it, so the light shines through the shell [13, 14]. Candling is an early example of a key AVI idea: the right illumination makes hidden defects visible. Such tasks are common in agribusiness, egg packing stations, food packaging plants, frozen and snack food manufacturing, and catering suppliers.

#### Plastic parts inspection

![3d-print-inspection](assets/3d-print-inspection.png)

*Figure 3. Manual inspection of plastic parts. Typical defects: excess plastic (flash), sink marks, and burn marks. Image generated with Gemini AI.*

Machine operators and quality technicians inspect plastic parts as they leave the production machine. The machine can be an injection-molding press, an extrusion line, or a 3D printer. Typical parts are automotive interior trim, appliance housings, containers, toys, and custom 3D-printed parts. For molded parts, inspectors look for five common defects [15]. Flash is excess plastic at the mold parting line. Sink marks are shallow dents above thick sections. Short shots are incompletely filled parts. Weld lines are visible lines where two melt fronts meet. Burn marks are dark spots caused by overheated material or trapped air. For 3D-printed parts, inspectors also look for warping, broken features, and surface defects [16]. Such tasks are common in automotive manufacturing, consumer electronics, toy production, medical disposables, and molding or 3D-printing service bureaus.

#### Textile and fabric quality grading

![textile-inspection](assets/textile-inspection.png)

*Figure 4. Manual fabric inspection on an illuminated inspection machine. Typical defects: stains, missing ends, and yarn lumps. Image generated with Gemini AI.*

Textile inspectors run large rolls of woven or knitted fabric through an illuminated inspection machine. The fabric moves past at eye level. Inspectors look for stains, holes, yarn lumps (slubs), missing ends (missing warp yarns), and shade variations [17]. They measure each flaw and assign penalty points. The most widely used scheme is the four-point system of ASTM D5430. Each defect receives 1 to 4 points, depending on its size and importance [18, 19]. A roll fails when its points per 100 square yards exceed a limit. Many factories use 40 points as the limit, but each buyer can set its own [19]. Such tasks are common in garment manufacturing, home textiles, technical textiles, and fabric distribution.

#### Structural infrastructure inspection

![structural-inspection](assets/structural-inspection.png)

*Figure 5. Visual inspection of a concrete and steel structure. Typical defects: cracks, corrosion, and deflection. Image generated with Gemini AI.*

Civil engineers and certified inspectors visually survey critical infrastructure. Examples are concrete bridges, highway overpasses, tunnels, retaining walls, and buildings. They use tools such as crack-width rulers, inspection hammers, and binoculars. They look for cracks, rust stains from corroding steel reinforcement, spalling (concrete breaking off the surface), excessive deflection (sagging), and joint deterioration [20, 21]. These inspections are often mandatory and periodic. In the USA, most highway bridges must be inspected at least every 24 months [22]. A large study by the US Federal Highway Administration (FHWA) asked 49 inspectors to rate the same bridges. The condition ratings of one bridge spanned up to five different values [23]. Such tasks are common in civil engineering consulting, public works, transportation departments, maintenance contractors, and facility management.

#### Pharmaceutical injectables inspection

![vial-inspection](assets/vial-inspection.png)

*Figure 6. Manual inspection of injectable vials against black and white backgrounds. Typical defects: particles, glass cracks, and wrong fill level. Image to be generated with Gemini AI.*

Every container of an injectable drug must be inspected before release. This is required by chapter <790> of the United States Pharmacopeia (USP) [24, 25]. Trained inspectors sit at an inspection booth. They inspect each vial, syringe, or ampoule under bright, flicker-free light of 2000 to 3750 lux [24, 26]. They gently swirl or invert the container. They watch it for about five seconds against a black background and five seconds against a white background [24]. The black background reveals light-colored particles. The white background reveals dark particles and discoloration. Inspectors look for particles, glass cracks and chips, wrong fill volume, discoloration, and closure defects, such as missing stoppers [25, 27]. Inspectors must pass regular vision tests. They qualify with test sets that contain known good and defective units [25]. Such tasks are common in pharmaceutical fill-finish plants, biotechnology companies, and contract manufacturers.

#### Electronic assembly inspection

![pcb-inspection](assets/pcb-inspection.png)

*Figure 7. Manual inspection of printed circuit board assemblies under a magnifier. Typical defects: solder bridges, tombstoned components, and insufficient solder. Image to be generated with Gemini AI.*

Electronics inspectors check printed circuit board assemblies (PCBAs) after soldering. They work at benches with illuminated magnifiers or stereo microscopes. They compare each board with the acceptance criteria of IPC-A-610, the industry standard for electronic assemblies [28]. They look for solder bridges between pins, insufficient or excess solder, tombstoning (a small component standing up on one end), and missing, misaligned, or reversed components [28, 29]. A modern board can carry thousands of tiny solder joints. This makes manual inspection slow and tiring. Such tasks are common in electronics manufacturing services, automotive electronics, medical devices, aerospace, and consumer electronics.

#### Automotive paint inspection

![paint-inspection](assets/paint-inspection.png)

*Figure 8. Manual inspection of a painted car body in a light tunnel. Typical defects: dirt inclusions, craters, and orange peel. Image to be generated with Gemini AI.*

Paint inspectors check every painted car body before final assembly. The body moves through a brightly lit inspection booth, often called a light tunnel. Inspectors walk around the body and keep changing their viewing angle. This is needed because small paint defects are only visible under directional light or at certain angles [30]. The most frequent defects are dirt inclusions and craters [30]. A dirt inclusion is a small bump in, on, or under the paint. A crater is a small bowl-shaped hole in the paint. Inspectors also judge the paint appearance and surface structure [31]. One example is orange peel, an uneven waviness that resembles the skin of an orange. They mark each defect for repair by sanding and polishing. Their evaluation is subjective and depends on the inspector's experience [30, 32]. Such tasks are common in car, truck, and agricultural-vehicle plants, and in other industries with high-gloss surfaces, such as home appliances.

### Automatic visual inspection

![avi-inspector](assets/avi-inspector.png)

*Figure 9. The AVI system. Cameras sense, processors decide, and actuators act.*

AVI is an industrial quality-control method. It combines dedicated illumination, optical imaging, and computer algorithms. Together, they evaluate products for defects, dimensional compliance, and surface anomalies. The evaluation is automatic, continuous, and fast enough to keep up with production [2, 3].

Figure 9 mirrors Figure 1. The camera replaces the eye. The processor and its algorithms replace the brain. A robot, a reject gate, or another actuator replaces the hands. In the lower panel, each product is described by numerical features computed from its images. Examples are sizes, contrasts, textures, or features learned by a neural network. Well-designed features separate the quality classes better than human perception does. Creating this separation is the central goal of the AVI design process in this document.

AVI matters for four reasons. First, it supports zero-defect manufacturing [6]. It finds defects in real time, so the process can be corrected immediately. This reduces scrap, saves material, and keeps defective products away from customers. Second, it makes 100% inspection feasible at line speed. Manual inspection, in contrast, often has to rely on sampling [11]. Third, it applies the same criteria on every shift. Human performance drops with fatigue and monotony [10, 33]. Fourth, it creates digital records. Every decision can be traced back to an image, a time, and a production batch.

AVI is not perfect. It can miss defects and reject good parts. It only detects what its sensors can see and what its algorithms were designed or trained for [34, 35]. The comparison section below discusses these trade-offs.

**Key terms used in this document**

| **Term** | **Meaning** |
| :--- | :--- |
| Machine vision | Engineering use of cameras, optics, and computer vision to solve industrial tasks [7]. |
| Escape (false negative) | A defective part that the inspection accepts. |
| False reject (false positive, overkill) | A good part that the inspection rejects. |
| Zero-defect manufacturing (ZDM) | A strategy to detect, repair, predict, and prevent defects [6]. |
| CAD model | Computer-aided design file that holds the nominal (ideal) geometry of a part. |
| Point cloud | A set of 3D points that samples the surface of an object. It is produced by 3D scanners or LiDAR. |
| Deflectometry | Measurement of a glossy surface by watching how it reflects a known light pattern. |
| SLAM | Simultaneous localization and mapping. A robot builds a map while it locates itself in that map. |
| PLC | Programmable logic controller. The industrial computer that controls machines on the line. |
| MES / ERP | Manufacturing execution system / enterprise resource planning. Software that tracks production and business data. |
| Human-in-the-loop | A design in which humans review machine decisions and feed corrections back into the system. |
| Cycle (takt) time | The time available to process one part. |

The automated examples below follow the order of the manual examples. The table summarizes the pairs. Each example ends with its key challenge. These challenges are discussed further in the applications section.

| **Inspection task** | **Manual example** | **Automated example** | **Main sensing principle** |
| :--- | :--- | :--- | :--- |
| Eggs | Food and egg inspection | Sanovo vision weighing | Multi-view cameras |
| Plastic and 3D-printed parts | Plastic parts inspection | AM-Flow AM-Quality | 3D scanning compared with CAD |
| Fabric | Textile and fabric grading | SUNTECH fabric inspection and packing | Cameras with controlled lighting |
| Buildings | Structural inspection | RaSpect indoor inspection | Mobile robot with cameras |
| Injectable drugs | Pharmaceutical injectables | Antares Vision C2 | Spinning containers and image sequences |
| Electronics | Electronic assembly | Koh Young Zenith 2 | 3D fringe projection |
| Car bodies | Automotive paint | Micro-Epsilon reflectCONTROL | Deflectometry |

#### Automated vision weighing in egg grading

Sanovo's egg grading line shows how AVI replaces mechanical scales and physical contact with optics [36, 37]. A sensor detects each incoming egg. Several high-resolution cameras capture images of each egg from defined angles. Together, the images cover the whole shell. Software extracts the size and shape of the egg from the images. A defined mathematical formula then converts these measurements into a weight. No scale or load cell is used [36]. Software evaluation of the same images also finds hairline cracks and leakers, which are eggs that leak liquid [36]. Sanovo markets the system as VisionAI [36, 37]. Operators can tune the detection and grading thresholds for both quality and weight classes [37].

**Key challenge:** natural products vary in color, size, and shape. The class "good egg" is therefore itself very wide.

[![Watch the video](https://img.youtube.com/vi/MXmqqQa043I/sddefault.jpg)](https://youtu.be/MXmqqQa043I)

#### Automated inline quality control of 3D-printed parts

AM-Flow's AM-Quality system shows inline inspection of plastic and 3D-printed parts [16, 38]. It replaces manual sampling with full inspection of every part. Parts travel on a conveyor through a scanning station. Eight high-speed coordinate measuring machines (CMMs) scan each part in 3D. They capture the full part geometry as a point cloud with about 50 µm accuracy [16]. Software compares the point cloud with the nominal digital model of the part, such as a CAD, STL, or STEP file. The differences reveal breakages, warping, and surface defects. The system returns an OK or Not-OK decision within a 5-second takt time. It handles up to 720 parts per hour [16]. It can also create a full metrology report for each part, which provides a complete audit trail [16].

**Key challenge:** in 3D printing, every part can be different. The system must inspect each part against its own reference model instead of learning one "good" part.

[![Watch the video](https://vumbnail.com/1019721995_large.jpg)](https://vimeo.com/1019721995)

#### Automated fabric inspection and packing

SUNTECH Automation's production line shows AVI in textile manufacturing [39]. It replaces manual inspection and sorting with an integrated, data-driven workflow. First, a vision system with cameras, controlled lighting, and machine learning detects fabric flaws in real time. It records the location and severity of each flaw. Second, a material-handling system aligns the fabric edges, controls the tension, and cuts, samples, and tapes the roll ends. Third, a labeling and sorting system adds barcodes and routes each roll to the correct quality grade. Fourth, a packaging station wraps the rolls in protective film. Finally, robotic stackers move the rolls. All data are linked to enterprise software for tracking and analytics [39]. Automated grading follows the same penalty-point logic that human inspectors use [17, 18].

**Key challenge:** wide fabric moves fast, and many defects have very low contrast against the fabric texture.

[![Watch the video](https://img.youtube.com/vi/7_0e6BIYZ6M/sddefault.jpg)](https://youtu.be/7_0e6BIYZ6M)

#### Indoor autonomous inspection

RaSpect's system shows autonomous inspection of buildings and facilities [40, 41]. It replaces manual walk-through surveys with an integrated, data-driven workflow. First, a robot navigates the facility on its own. It uses SLAM to build a map while it locates itself and plans its path [41]. Second, the robot's cameras capture images and structural data from every corner of the facility. Third, the data are uploaded to a cloud platform. There, machine learning models flag defects, such as cracks, spalling, debonding, and wear, as well as safety hazards [40, 41]. Finally, an analytics platform turns the results into standard, repeatable digital surveys. These surveys support long-term trend analysis and simplify compliance checks [41].

**Key challenge:** lighting, viewing distance, and viewing angle are not controlled, unlike on a factory line.

[![Watch the video](https://img.youtube.com/vi/cVAnaEyF7rw/hqdefault.jpg)](https://youtu.be/cVAnaEyF7rw)

#### Automated inspection of injectable vials

Antares Vision's C2 machine shows automated inspection of injectable vials [42, 43]. Automated machines typically spin each container and then stop it abruptly. The liquid keeps moving while the glass stands still. Cameras record a sequence of images. Moving particles then stand out against fixed marks on the glass [27]. High-resolution cameras with tailored lighting also check cosmetic defects, fill level, and the aluminum crimp and stopper [42]. High-voltage leak detection finds micro-cracks and pinholes [42]. Machines of this family inspect 200 to 350 containers per minute. AI is used to reduce false rejects [42]. An automated system must be shown to perform at least as well as qualified human inspectors. Both are tested with the same sets of known defective units [25, 27].

**Key challenge:** air bubbles, glass reflections, and marks on the container can look like particles and cause false rejects.

[![Watch the video](https://img.youtube.com/vi/Rv1yaHq_Qqk/hqdefault.jpg)](https://youtu.be/Rv1yaHq_Qqk)

#### Automated optical inspection of electronic assemblies

Koh Young's Zenith 2 shows 3D automated optical inspection (AOI) of printed circuit board assemblies [29, 44]. The system projects moiré fringe patterns onto the board from several directions. Cameras record how the patterns bend over components and solder. From this, the system computes a true 3D height profile of the board [29]. It measures the height, volume, and coplanarity of every solder joint and component. It detects lifted leads, insufficient solder, solder bridges, tombstoning, polarity errors, and missing or misaligned components. Classical 2D AOI relies only on color and contrast. It is therefore more sensitive to lighting, reflections, and board variation. 3D measurement reduces both false calls and escapes [29].

**Key challenge:** shiny solder, tiny components, and dense boards push optics, resolution, and speed to their limits.

[![Watch the video](https://img.youtube.com/vi/5gWyXXX8iKA/hqdefault.jpg)](https://youtu.be/5gWyXXX8iKA)

#### Automated paint defect inspection

Micro-Epsilon's reflectCONTROL system shows automated inspection of painted car bodies [31, 45]. The system uses deflectometry. A screen displays a striped light pattern. Cameras observe the reflection of this pattern on the glossy paint. A defect bends the surface locally, so it distorts the reflected stripes [31]. Two to four sensors mounted on robots scan the car body. Each defect is located within ±3 mm. It is described by its height, depth, and volume [31]. The results are sent to robots that sand and polish each defect automatically. The same images are also used to evaluate the paint appearance [31].

**Key challenge:** mirror-like surfaces hide defects in normal camera images. The illumination principle itself must change.

[![Watch the video](https://img.youtube.com/vi/tig6Rb4g9aI/hqdefault.jpg)](https://youtu.be/tig6Rb4g9aI)

## Comparison between manual and automatic visual inspection

The table below compares manual inspection with AVI on ten dimensions. Scores range from 0 (very poor) to 5 (excellent). They are expert estimates based on the author's past projects. Where possible, they are supported by the published studies cited in the table. Figure 10 shows the same scores as a radar (spider) chart. Each axis is one dimension. The further a shape reaches along an axis, the better that approach performs on that dimension.

| **Feature** | **Manual inspection (Human)** | **Score (0-5)** | **Automatic visual inspection (AVI)** | **Score (0-5)** |
| :--- | :--- | :---: | :--- | :---: |
| D1 \| Speed and throughput | Limited by human reaction time and endurance. It creates bottlenecks on fast lines. | 1 | Very high. Systems inspect hundreds to thousands of parts per minute, for example 200 to 350 vials per minute [42]. | 5 |
| D2 \| Consistency and repeatability | Varies between people and over a shift. Ratings of the same bridge spanned up to five values [23]. | 2 | Applies the same rules every time. This holds while lighting, optics, and products stay within the validated range. | 5 |
| D3 \| Objectivity and bias | Subjective. Depends on experience, mood, stress, and personal thresholds [30]. | 2 | Free of mood and fatigue. It still inherits the bias of its thresholds and training labels [35]. | 4 |
| D4 \| Fatigue and vigilance | Detection drops during long, monotonous watching [10, 33]. | 1 | Runs 24/7 without fatigue or loss of attention. | 5 |
| D5 \| Cost structure | Low initial cost. High ongoing labor cost and costly escapes. | 3 | High initial investment in hardware, software, and integration. Low cost per inspected unit. | 4 |
| D6 \| Adaptability to new defects | High. Humans can reason about unexpected or new defect types. | 5 | Limited. Rule-based and supervised systems find only known defects. Unsupervised anomaly detection can flag new deviations but cannot explain them [34]. | 2 |
| D7 \| Data and traceability | Relies on manual records or paper checklists. Root-cause analysis is difficult. | 1 | Logs every decision with images and metrics in real time. | 5 |
| D8 \| Detection performance | In one controlled study, inspectors caught about 85% of defects but rejected about 35% of good parts [5]. Some studies suggest that error rates may reach 20 to 30% [46]. | 2 | High and measurable when well designed. It supports precise metrology, for example about 50 µm in 3D [16]. | 4 |
| D9 \| Sensing range | Visible light only. Limited resolution and no direct 3D measurement. | 1 | Can use near-infrared, ultraviolet, X-ray, thermal, and 3D sensors beyond human vision [3]. | 5 |
| D10 \| Setup and changeover effort | Inspectors can be trained in about two weeks [25]. They switch products quickly. | 4 | Each new product needs optics design, data collection, labeling, integration, and validation. | 2 |

![spider-avi](assets/spider-avi-v2.png)

*Figure 10. Radar chart of the scores in the table above.*

The comparison shows complementary strengths. AVI wins on speed, consistency, endurance, traceability, and sensing range. Humans win on adaptability and fast changeover. For this reason, many industrial systems are hybrid [46]. AVI makes most of the decisions. Humans review uncertain cases, investigate new defect types, and label data to improve the models. This human-centric view is also promoted by the Industry 5.0 strategy [47]. It is the basis of steps (7) and (S) of the design process below.

A fair comparison measures both approaches in the same way. Three metrics are common. The detection rate is the share of defective parts that are rejected. The escape rate is the share of defective parts that are accepted. The false reject rate is the share of good parts that are rejected. These rates are measured with a test set of parts whose true condition is known. In attribute agreement analysis, each inspector or system classifies the test set several times. The results show both accuracy and repeatability [48]. The pharmaceutical industry uses the same idea to qualify both human inspectors and machines [25, 27].

## Visual inspection design process

![design-process](assets/design-process.png)

*Figure 11. The canonical AVI design process. It has seven main steps and one supporting step.*

The AVI design process turns physical products into actionable quality decisions. Figure 11 shows the process model used in this document. It follows the processing chain found in standard machine-vision references [3, 7, 8]. It has seven main steps and one supporting step.

Before step (1), the designer must define the requirements. These include the defect catalogue with limit samples, the tolerances, the required detection and false reject rates, the cycle time, and the interfaces to the production line [49]. Every later design choice is checked against these requirements.

- **(1) Image capture** converts each part into digital images or 3D point clouds. Cameras, lenses, and illumination are chosen to make defects clearly visible. Hardware triggers and strobe lighting synchronize the capture with the moving part.
- **(2) System calibration** relates image measurements to the real world. It corrects lens distortion, defines the pixel-to-millimeter mapping, and aligns cameras and lighting across stations. Calibration is done at commissioning. It is checked periodically with reference targets.
- **(3) Image enhancement and pre-processing** improves image quality before analysis. Typical operations are noise filtering, contrast normalization, and image alignment. For 3D data, it removes outliers from point clouds.
- **(4) Region of interest and object detection** separates the target part or feature from the background. It uses classical methods, such as template matching, or deep learning, such as segmentation networks.
- **(5) Feature extraction and anomaly detection** finds known defects and unknown anomalies, and measures dimensions. It combines rule-based algorithms with supervised and unsupervised machine learning.
- **(6) Decision fusion and post-processing** combines all results into one decision: Pass, Fail, or Review. It fuses information from several views, sensors, or time steps. It also suppresses false alarms.
- **(7) Action and closed feedback loop** executes the decision. It sorts parts, logs data, and triggers alerts, for example through a PLC. It also sends uncertain and rejected cases to human reviewers.
- **(S) Model sandbox** is the supporting step. Here, human experts label new and difficult images. The labels are used to retrain and validate the models offline, for example with active learning. Validated updates are then deployed back to steps (3) to (6). The sandbox keeps the system improving after deployment.

The table summarizes the objective and typical industrial examples of each step.

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

The process is iterative. Problems found in later steps often require changes to earlier ones. For example, a defect that is hard to detect is often solved with better lighting in step (1), not with a more complex algorithm in step (5) [3]. The following sections detail each step.

### (1) Image capture

⚠️WARNING: Place holder for the image capture design process.⚠️

### (2) System calibration

⚠️WARNING: Place holder for the system calibration design process.⚠️

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

⚠️WARNING: Place holder for the best practices design process.⚠️

### Conclusions

⚠️WARNING: Place holder for the conclusions design process.⚠️

## References

[1] R. T. Chin and C. A. Harlow, "Automated visual inspection: A survey," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. PAMI-4, no. 6, pp. 557–573, 1982. https://doi.org/10.1109/TPAMI.1982.4767309  
[2] T. S. Newman and A. K. Jain, "A survey of automated visual inspection," *Computer Vision and Image Understanding*, vol. 61, no. 2, pp. 231–262, 1995. https://doi.org/10.1006/cviu.1995.1017  
[3] J. Beyerer, F. Puente León, and C. Frese, *Machine Vision: Automated Visual Inspection: Theory, Practice and Applications*. Berlin, Germany: Springer, 2016. https://doi.org/10.1007/978-3-662-47794-6  
[4] T. Czimmermann, G. Ciuti, M. Milazzo, M. Chiurazzi, S. Roccella, C. M. Oddo, and P. Dario, "Visual-based defect detection and classification approaches for industrial applications—A survey," *Sensors*, vol. 20, no. 5, art. 1459, 2020. https://doi.org/10.3390/s20051459  
[5] J. E. See, "Visual inspection reliability for precision manufactured parts," *Human Factors*, vol. 57, no. 8, pp. 1427–1442, 2015. https://doi.org/10.1177/0018720815602389  
[6] F. Psarommatis, G. May, P.-A. Dreyfus, and D. Kiritsis, "Zero defect manufacturing: State-of-the-art review, shortcomings and future directions in research," *International Journal of Production Research*, vol. 58, no. 1, pp. 1–17, 2020. https://doi.org/10.1080/00207543.2019.1605228  
[7] C. Steger, M. Ulrich, and C. Wiedemann, *Machine Vision Algorithms and Applications*, 2nd ed. Weinheim, Germany: Wiley-VCH, 2018.  
[8] B. G. Batchelor, Ed., *Machine Vision Handbook*. London, UK: Springer, 2012. https://doi.org/10.1007/978-1-84996-169-1  
[9] C. G. Drury and J. G. Fox, Eds., *Human Reliability in Quality Control*. London, UK: Taylor & Francis, 1975.  
[10] J. E. See, "Visual inspection: A review of the literature," Sandia National Laboratories, Albuquerque, NM, USA, Rep. SAND2012-8590, 2012. https://www.osti.gov/biblio/1055636  
[11] ISO 2859-1:1999/Amd 1:2011, *Sampling procedures for inspection by attributes — Part 1: Sampling schemes indexed by acceptance quality limit (AQL) for lot-by-lot inspection*. Geneva, Switzerland: International Organization for Standardization, 1999; Amendment 1, 2011.  
[12] T. Brosnan and D.-W. Sun, "Improving quality inspection of food products by computer vision—a review," *Journal of Food Engineering*, vol. 61, no. 1, pp. 3–16, 2004. https://doi.org/10.1016/S0260-8774(03)00183-3  
[13] U.S. Department of Agriculture, Agricultural Marketing Service, *Egg-Grading Manual*, Agricultural Handbook No. 75. Washington, DC, USA: USDA, 2000.  
[14] National 4-H Poultry and Egg Conference, University of Kentucky, "Market eggs: Interior egg grading by candling." https://national4hpoultry.mgcafe.uky.edu/marketeggs/candling (Accessed Oct. 19, 2026.)  
[15] BASF, *Injection Molding Problems in Engineering Thermoplastics: Causes and Solutions* (technical brochure). Ludwigshafen, Germany: BASF SE, Aug. 2009. https://download.basf.com/p1/8a8082587fd4b608017fd6631d5a24b1/en/Injection-Molding_Problems_in_Engineering_Thermoplastics_-_Causes_and_Solutions_Brochure_English.pdf (Accessed Oct. 19, 2026.)  
[16] 3D ADEPT Media, "AM-Flow unveils an enhanced version of its AM-Quality solution," Nov. 12, 2024. https://3dadept.com/am-flow-unveils-an-enhanced-version-of-its-am-quality-solution/  
[17] A. Kumar, "Computer-vision-based fabric defect detection: A survey," *IEEE Transactions on Industrial Electronics*, vol. 55, no. 1, pp. 348–363, 2008.  
[18] ASTM D5430-26, *Standard Test Methods for Visually Inspecting and Grading Fabrics*. West Conshohocken, PA, USA: ASTM International, 2026.  
[19] V-Trust Inspection Service, "Understanding the 4-point system for fabric inspections," Mar. 30, 2025. https://www.v-trust.com/en/blog/understanding-the-4-point-system-for-fabric-inspections (Accessed Oct. 19, 2026.)  
[20] C. Koch, K. Georgieva, V. Kasireddy, B. Akinci, and P. Fieguth, "A review on computer vision based defect detection and condition assessment of concrete and asphalt civil infrastructure," *Advanced Engineering Informatics*, vol. 29, no. 2, pp. 196–210, 2015. https://doi.org/10.1016/j.aei.2015.01.008  
[21] B. F. Spencer Jr., V. Hoskere, and Y. Narazaki, "Advances in computer vision-based civil infrastructure inspection and monitoring," *Engineering*, vol. 5, no. 2, pp. 199–222, 2019. https://doi.org/10.1016/j.eng.2018.11.030  
[22] Federal Highway Administration, "National Bridge Inspection Standards, inspection interval guidance," memorandum, Office of Bridges and Structures, Jun. 13, 2022. https://www.fhwa.dot.gov/bridge/pubs/memo_inspection_interval_guidance.pdf  
[23] M. Moore, B. Phares, B. Graybeal, D. Rolander, and G. Washer, *Reliability of Visual Inspection for Highway Bridges, Volume I: Final Report*, Rep. FHWA-RD-01-020. McLean, VA, USA: Federal Highway Administration, 2001. https://www.fhwa.dot.gov/publications/research/nde/pdfs/01020a.pdf  
[24] United States Pharmacopeia, General Chapter <790> *Visible Particulates in Injections*. Rockville, MD, USA: USP.  
[25] J. G. Shabushnig (Insight Pharma Consulting, LLC), "Visual inspection of injectable products: More than sorting good from bad," presentation slides, Sep. 2022. Hosted by the U.S. Food and Drug Administration. https://www.fda.gov/media/162175/download  
[26] CAI, "Implementing USP visual inspection requirements," Nov. 21, 2017. https://caiready.com/life-sciences/blog/implementing-usp-visual-inspection-requirements/ (Accessed Oct. 19, 2026.)  
[27] United States Pharmacopeia, General Chapter <1790> *Visual Inspection of Injections*. Rockville, MD, USA: USP.  
[28] IPC, *IPC-A-610J: Acceptability of Electronic Assemblies*. Bannockburn, IL, USA: IPC, 2024. Release note: https://www.electronics.org/news-release/ipc-releases-j-revisions-two-leading-standards-electronics-assembly  
[29] Koh Young America, "Guide to automated optical inspection (AOI) with Koh Young's 3D AOI solutions," Jun. 25, 2025. https://kohyoungamerica.com/guide-to-automated-optical-inspection-aoi-with-koh-youngs-3d-aoi-solutions/ (Accessed Oct. 19, 2026.)  
[30] N. Pya Arnqvist, B. Ngendangenzwa, E. Lindahl, L. Nilsson, and J. Yu, "Effective degrees of freedom for surface finish defect detection and classification," arXiv:1906.11904, 2019. https://arxiv.org/abs/1906.11904  
[31] K. Steinhuber (Micro-Epsilon), "Paint defect inspection in automotive production: Visualization of reflective surfaces using deflectometry," *Wiley Industry News*, May 23, 2025. https://wileyindustrynews.com/en/contributions/paint-defect-inspection-in-automotive-production (Accessed Oct. 19, 2026.)  
[32] J. Molina, J. E. Solanes, L. Arnal, and J. Tornero, "On the detection of defects on specular car body surfaces," *Robotics and Computer-Integrated Manufacturing*, vol. 48, pp. 263–278, 2017. https://doi.org/10.1016/j.rcim.2017.04.009  
[33] N. H. Mackworth, "The breakdown of vigilance during prolonged visual search," *Quarterly Journal of Experimental Psychology*, vol. 1, no. 1, pp. 6–21, 1948. https://doi.org/10.1080/17470214808416738  
[34] P. Bergmann, M. Fauser, D. Sattlegger, and C. Steger, "MVTec AD — A comprehensive real-world dataset for unsupervised anomaly detection," in *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2019, pp. 9584–9592. https://doi.org/10.1109/CVPR.2019.00982  
[35] Y. Cheng, Y. Cao, H. Yao, et al., "A comprehensive survey for real-world industrial defect detection: Challenges, approaches, and prospects," arXiv:2507.13378, 2025. https://arxiv.org/abs/2507.13378  
[36] SANOVO TECHNOLOGY GROUP, "Vision weighing in egg grading." https://www.sanovogroup.com/en/egg/knowledge/knowledge-library/vision-weighing-in-egg-grading/ (Accessed Oct. 19, 2026.)  
[37] SANOVO TECHNOLOGY GROUP, "Vision weighing in egg grading | Contactless weight detection without scales | SANOVO (2026)," video, YouTube, Feb. 5, 2026. https://youtu.be/MXmqqQa043I  
[38] AM-Flow, "AM-QUALITY – The world's first in-line quality control solution," video, Vimeo, Oct. 15, 2024. https://vimeo.com/1019721995  
[39] SUNTECH Automation, "AI fabric inspection & automated packing solutions | Maximize your ROI | Save labor & time," video, YouTube, Jan. 23, 2025. https://youtu.be/7_0e6BIYZ6M  
[40] Electrical and Mechanical Services Department (EMSD), Hong Kong SAR Government, "AI-powered robotic autonomous inspection system" (RaSpect Intelligence Inspection Ltd.), I&T solution listing, Nov. 12, 2019. https://inno.emsd.gov.hk/en/it-solutions/index_id_380.html (Accessed Oct. 19, 2026.)  
[41] RaSpect, "AI-driven indoor autonomous inspection," video, YouTube, Mar. 27, 2026. https://youtu.be/cVAnaEyF7rw  
[42] Antares Vision Group, "Advanced vial inspection machines," Apr. 17, 2026. https://antaresvisiongroup.com/lifescience/advanced-vial-inspection-machines-antares-vision-group/ (Accessed Oct. 19, 2026.)  
[43] Antares Vision Group | Life Science, "C2 automatic visual inspection machine for vials," video, YouTube, Jun. 19, 2024. https://youtu.be/Rv1yaHq_Qqk  
[44] Koh Young Technology, Inc., "Koh Young Technology - Zenith 2 (3D AOI)," video, YouTube, Sep. 26, 2021. https://youtu.be/5gWyXXX8iKA  
[45] Micro-Epsilon Messtechnik, "Fully automated surface inspection with reflectCONTROL," video, YouTube, Sep. 9, 2025. https://youtu.be/tig6Rb4g9aI  
[46] A. Kujawińska and K. Vogt, "Human factors in visual quality control," *Management and Production Engineering Review*, vol. 6, no. 2, pp. 25–31, 2015. https://doi.org/10.1515/mper-2015-0013  
[47] European Commission, Directorate-General for Research and Innovation, M. Breque, L. De Nul, and A. Petridis, *Industry 5.0: Towards a Sustainable, Human-Centric and Resilient European Industry*. Luxembourg: Publications Office of the European Union, Jan. 2021. https://research-and-innovation.ec.europa.eu/knowledge-publications-tools-and-data/publications/all-publications/industry-50_en  
[48] Automotive Industry Action Group (AIAG), *Measurement Systems Analysis (MSA) Reference Manual*, 4th ed. Southfield, MI, USA: AIAG, 2010.  
[49] VDI/VDE/VDMA 2632 Part 2:2015-10, *Machine vision — Guideline for the preparation of a requirement specification and a system specification*. Berlin, Germany: Beuth Verlag (now DIN Media), 2015. Withdrawn and replaced by VDI/VDE/VDMA 2632 Part 2:2024-11.  
