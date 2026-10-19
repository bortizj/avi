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

## Definitions and purpose

In this section we define manual (classical) and automatic visual inspection, each followed by a few industrial examples. The examples are paired, i.e., each automated example solves the same inspection task as one of the manual examples.

### Classical visual inspection

![human-inspector](assets/human-inspector.png)

*Figure 1. The human inspector as an inspection system, where the eye senses, the brain decides, and the hands act.*

Before defining what automatic visual inspection involves, it is important to understand what human-based inspection involves (classical or manual visual inspection). Visual inspection is the process of examining products, components, or structures using the human eye to detect flaws, defects, or non-compliance with quality standards [9, 10]. Inspectors are often aided by controlled lighting, magnifiers, gauges, or simple hand tools.

Figure 1 shows the human inspector as a three-part system. The eye captures the visual information, the brain compares what it sees against a mental model of a good part, and the hands act on the decision, e.g., by removing a part from the line. The lower panel shows a simplified quality inspection space, where each dot is one product described by the visual features the inspector perceives and each color is one quality class. The classes overlap, which is one of the reasons why decisions vary from inspector to inspector and over time [5].

Manual inspection is typically done in two ways, i.e., 100% inspection, where every unit is checked, and sampling inspection, where only a random sample of each lot is checked. In sampling inspection, the whole lot is then accepted or rejected based on the sample, e.g., using the sampling plans of ISO 2859-1 [11]. Below we list a few examples of classical visual inspection tasks across different industries.

#### Food and egg inspection and sorting

![eggs-inspection](assets/eggs-inspection.png)

*Figure 2. Manual egg grading on a conveyor with typical defects such as rough shells, blood spots, and soft shells. The image in this example was generated using Gemini AI.*

Quality control sorters (line workers) stand alongside moving conveyor belts to manually inspect raw or semi-processed agricultural goods, e.g., eggs, fresh fruits, root vegetables, nuts, bakery items. Their task is to scan for and discard bruised, rotting, or misshapen produce, alongside foreign contaminants, e.g., stones, stems, dirt clumps, or pieces of field debris [12]. In egg grading, inspectors additionally check the shell for cracks, dirt, rough texture, and soft or thin shells [13]. Internal defects such as blood spots are invisible under normal light; therefore, inspectors find them by candling. Candling consists of holding the egg against a bright light in a dark room and rotating it so the light shines through the shell [13, 14]. Candling is an early example of a key AVI idea, that is, the right illumination makes hidden defects visible. Such tasks are common in agribusiness, egg packing stations, food packaging plants, frozen and snack food manufacturing, and catering suppliers.

#### Plastic parts inspection

![3d-print-inspection](assets/3d-print-inspection.png)

*Figure 3. Manual inspection of plastic parts with typical defects such as excess plastic (flash), sink marks, and burn marks. The image in this example was generated using Gemini AI.*

Machine operators and / or quality control technicians visually inspect plastic parts, e.g., automotive interior trim, appliance housings, plastic containers, toys, or custom 3D-printed parts. This is typically done as the produced goods emerge from injection molding presses, extrusion lines, or 3D printers. For molded parts, inspectors check for common surface defects, i.e., sink marks, short shots, and burn marks [15]. Sink marks are shallow dents above thick sections. Short shots are incompletely filled parts, and burn marks are dark spots caused by overheated material or trapped air. For 3D-printed parts, inspectors additionally look for warping, broken features, and surface defects [16]. Such tasks are common in automotive manufacturing, consumer electronics, toy production, medical disposables, and molding or 3D-printing services.

#### Textile and fabric quality grading

![textile-inspection](assets/textile-inspection.png)

*Figure 4. Manual fabric inspection on an illuminated inspection machine with typical defects such as stains, missing ends, and yarn lumps. The image in this example was generated using Gemini AI.*

Textile examiners feed large rolls of woven or knitted fabric through an illuminated inspection machine or board. As the fabric moves past at eye level, inspectors scan for irregularities such as stains, holes, yarn lumps (slubs), missing ends (missing warp yarns), and shade variations [17]. They measure flaw sizes and apply standardized penalty points to determine if a roll passes quality thresholds. The most widely used scheme is the four-point system of ASTM D5430, where each defect receives 1 to 4 points depending on its size and importance [18, 19]. A roll fails when its points per 100 square yards exceed a limit, which many factories set at 40 points, although each buyer can set its own [19]. Such tasks are common in garment manufacturing, home textiles, technical textiles, and fabric distribution.

#### Structural infrastructure inspection

![structural-inspection](assets/structural-inspection.png)

*Figure 5. Visual inspection of a concrete and steel structure with typical defects such as cracks, corrosion, and deflection. The image in this example was generated using Gemini AI.*

Civil engineers and certified structural inspectors conduct visual surveys of critical infrastructure, e.g., concrete bridges, highway overpasses, tunnels, retaining walls, and buildings. Using specialized tools like crack-width rulers, inspection hammers, and binoculars, they inspect surfaces for signs of structural cracking, rust bleeding from corroding steel reinforcement, spalling (concrete breaking off the surface), excessive deflection (sagging), and joint deterioration [20, 21]. These inspections are often mandatory and periodic, e.g., in the USA, most highway bridges must be inspected at least every 24 months [22]. However, their outcome strongly depends on the inspector. For example, in a large study of the US Federal Highway Administration (FHWA), 49 inspectors rated the same bridges, and the condition ratings of a single bridge spanned up to five different values [23]. Such tasks are common in civil engineering consulting, public works, transportation departments, maintenance contractors, and facility management.

#### Pharmaceutical injectables inspection

![vial-inspection](assets/vial-inspection.png)

*Figure 6. Manual inspection of injectable vials against black and white backgrounds with typical defects such as particles, glass cracks, and wrong fill level. The image in this example was generated using Gemini AI.*

Every container of an injectable drug must be inspected before release, as required by chapter <790> of the United States Pharmacopeia (USP) [24, 25]. Trained inspectors sit at an inspection booth and examine each vial, syringe, or ampoule under bright, flicker-free light of 2000 to 3750 lux [24, 26]. They gently swirl or invert the container and watch it for about five seconds against a black background and five seconds against a white background [24]. The black background reveals light-colored particles, while the white background reveals dark particles and discoloration. Inspectors look for particles, glass cracks and chips, wrong fill volume, discoloration, and closure defects, e.g., missing stoppers [25, 27]. Additionally, inspectors must pass regular vision tests and qualify using test sets that contain known good and defective units [25]. Such tasks are common in pharmaceutical fill-finish plants, biotechnology companies, and contract manufacturers.

#### Electronic assembly inspection

![pcb-inspection](assets/pcb-inspection.png)

*Figure 7. Manual inspection of printed circuit board assemblies under a magnifier with typical defects such as solder bridges, tombstoned components, and insufficient solder. The image in this example was generated using Gemini AI.*

Electronics inspectors check printed circuit board assemblies (PCBAs) after soldering, typically working at benches with illuminated magnifiers or stereo microscopes. They compare each board against the acceptance criteria of IPC-A-610, the industry standard for electronic assemblies [28]. Inspectors scan for solder bridges between pins, insufficient or excess solder, tombstoning (a small component standing up on one end), and missing, misaligned, or reversed components [28, 29]. Since a modern board can carry thousands of tiny solder joints, manual inspection quickly becomes slow and tiring. Such tasks are common in electronics manufacturing services, automotive electronics, medical devices, aerospace, and consumer electronics.

#### Automotive paint inspection

![paint-inspection](assets/paint-inspection.png)

*Figure 8. Manual inspection of a painted car body in a light tunnel with typical defects such as dirt inclusions, craters, and orange peel. The image in this example was generated using Gemini AI.*

Paint inspectors check every painted car body before final assembly. As the body moves through a brightly lit inspection booth, often called a light tunnel, inspectors walk around it and keep changing their viewing angle. This is necessary since small paint defects are only visible under directional light or at certain angles [30]. The most frequent defects are dirt inclusions, i.e., small bumps in, on, or under the paint, and craters, i.e., small bowl-shaped holes in the paint [30]. Inspectors also judge the paint appearance and surface structure, e.g., orange peel, an uneven waviness that resembles the skin of an orange [31]. Each defect is then marked for repair by sanding and polishing. This evaluation is subjective and depends on the inspector's experience [30, 32]. Such tasks are common in car, truck, and agricultural-vehicle plants, and in other industries with high-gloss surfaces such as home appliances.

### Automatic visual inspection

![avi-inspector](assets/avi-inspector.png)

*Figure 9. The AVI system, where cameras sense, processors decide, and robotic components act.*

AVI is an industrial quality-control methodology that integrates dedicated illumination, optical imaging, and computational algorithms to automatically and continuously evaluate products for defects, dimensional compliance, and surface anomalies at production speed [2, 3].

Figure 9 mirrors Figure 1, i.e., the camera replaces the eye, the processor and its algorithms replace the brain, and a robot, a reject gate, or another actuator replaces the hands. In the lower panel, each product is described by numerical features computed from its images, e.g., sizes, contrasts, textures, or features learned by a neural network. Well-designed features separate the quality classes better than human perception does. Therefore, creating this separation is the central goal of the AVI design process described in this document.

AVI is important for four main reasons. First, it supports zero-defect manufacturing strategies [6], since automated systems detect defects in real time, enabling immediate corrective actions that reduce scrap rates, optimize material usage, and prevent defective products from reaching consumers. Second, it makes inspection feasible at line speed, whereas manual inspection often has to rely on sampling [11]. Third, it maintains uniform evaluation criteria on every shift, avoiding the performance degradation associated with operator fatigue and monotony [10, 33]. Fourth, it provides traceable digital records, where every decision can be traced back to an image, a time, and a production batch.

However, AVI also has its limitations. AVI systems can miss defects and reject good parts, since they only detect what their sensors can see and what their algorithms were designed or trained for [34, 35]. These trade-offs are discussed in more detail in the comparison section below.

#### Automated vision weighing in egg grading

To see how AVI works in practice in food inspection, we can examine Sanovo's egg grading workflow, which replaces traditional mechanical scales and physical touch points with a contactless optical module [36, 37]. First, a built-in sensor detects each incoming egg while an array of high-resolution cameras captures images of each egg from defined angles for complete surface coverage. Next, software extracts the size and shape of the egg from the images, and a defined mathematical formula converts these measurements into a weight without the need for a scale or load cell [36]. Alongside this, a software evaluation of the same images isolates anomalies like hairline cracks and leakers, i.e., eggs that leak liquid [36]. Sanovo markets this system as VisionAI [36, 37]. Finally, a control and classification system allows operators to fine-tune detection and grading thresholds for both quality and weight classes [37].

[![Watch the video](https://img.youtube.com/vi/MXmqqQa043I/hqdefault.jpg)](https://youtu.be/MXmqqQa043I)

#### Automated inline quality control of 3D-printed parts

To see how automated inline quality control works in practice for plastic and 3D-printed parts, we can look at the AM-Flow AM-Quality system, which replaces traditional manual sampling with full inspection of every part [16, 38]. First, parts travel on a conveyor through a scanning station, where eight high-speed coordinate measuring machines (CMMs) scan each part in 3D to capture its complete geometry as a point cloud with about 50 µm accuracy [16]. Next, a digital inspection engine compares the point cloud against the nominal digital model of the part, e.g., a CAD, STL, or STEP file, revealing breakages, warping, and surface defects. The system then returns an OK or Not-OK decision [16]. Finally, a reporting system can generate a full metrology report per part for complete audit trails [16].

[![Watch the video](https://vumbnail.com/1019721995_medium.jpg)](https://vimeo.com/1019721995)

#### Automated fabric inspection and packing

To see how AVI works in practice in textile manufacturing, we can look at SUNTECH Automation's production line, which replaces traditional manual inspection and sorting with an integrated data-driven workflow [39]. First, a visual inspection system uses cameras, controlled lighting, and machine learning to catch fabric flaws in real time, recording their location and severity. Alongside it, a material-handling system keeps the fabric moving by automating edge alignment, tension control, cutting, sampling, and roll-end taping. Afterwards, an automated labeling and sorting system adds tracking barcodes and routes each roll into the correct quality grade. From there, a packaging station wraps the rolls in protective film. Finally, robotic stackers handle the transport, while all shop-floor data are linked to enterprise software for complete tracking and analytics [39]. Note that the automated grading follows the same penalty-point logic used by human inspectors [17, 18].

[![Watch the video](https://img.youtube.com/vi/7_0e6BIYZ6M/hqdefault.jpg)](https://youtu.be/7_0e6BIYZ6M)

#### Indoor autonomous inspection

To see how autonomous inspection works in practice, we can look at RaSpect's system, which replaces traditional manual facility walk-throughs with an integrated data-driven workflow [40, 41]. First, an autonomous navigation system uses SLAM and path planning to build a map of the facility while the robot locates itself in it [41]. Alongside it, the robot's cameras capture images and structural data from every corner of the facility. Afterwards, the captured data are uploaded to a cloud platform, where machine learning models automatically flag defects, e.g., cracks, spalling, debonding, and wear, as well as safety hazards [40, 41]. From there, an analytics platform turns these results into standardized, repeatable digital surveys that enable long-term trend analysis and simplify compliance checks [41].

[![Watch the video](https://img.youtube.com/vi/cVAnaEyF7rw/hqdefault.jpg)](https://youtu.be/cVAnaEyF7rw)

#### Automated inspection of injectable vials

To see how AVI works in practice in pharmaceutical manufacturing, we can look at Antares Vision's C2 machine for injectable vials [42, 43]. Automated machines of this type typically spin each container and then stop it abruptly, so the liquid keeps moving while the glass stands still. Cameras then record a sequence of images in which moving particles stand out against fixed marks on the glass [27]. Additionally, high-resolution cameras with tailored lighting check cosmetic defects, fill level, and the aluminum crimp and stopper, while high-voltage leak detection finds micro-cracks and pinholes [42]. Note that an automated system must be shown to perform at least as well as qualified human inspectors, where both are tested using the same sets of known defective units [25, 27].

[![Watch the video](https://img.youtube.com/vi/Rv1yaHq_Qqk/hqdefault.jpg)](https://youtu.be/Rv1yaHq_Qqk)

#### Automated optical inspection of electronic assemblies

To see how AVI works in practice in electronics manufacturing, we can look at Koh Young's Zenith 2, a 3D automated optical inspection (AOI) system for printed circuit board assemblies [29, 44]. First, the system projects moiré fringe patterns onto the board from several directions, while cameras record how the patterns bend over components and solder. From this, the system computes a true 3D height profile of the board [29]. Next, it measures the height, volume, and coplanarity of every solder joint and component to detect lifted leads, insufficient solder, solder bridges, tombstoning, polarity errors, and missing or misaligned components. In contrast, classical 2D AOI relies only on color and contrast, which makes it more sensitive to lighting, reflections, and board variation. Therefore, 3D measurement reduces both false calls and escapes [29].

[![Watch the video](https://img.youtube.com/vi/5gWyXXX8iKA/hqdefault.jpg)](https://youtu.be/5gWyXXX8iKA)

#### Automated paint defect inspection

To see how AVI works in practice in automotive manufacturing, we can look at Micro-Epsilon's reflectCONTROL system for painted car bodies [31, 45]. The system uses deflectometry, where a screen displays a striped light pattern and cameras observe its reflection on the glossy paint. Since a defect locally bends the surface, it distorts the reflected stripes [31]. First, two to four robot-mounted sensors scan the car body, locating each defect within ±3 mm and describing it by its height, depth, and volume [31]. Afterwards, the results are sent to robots that automatically sand and polish each defect. Additionally, the same images are used to evaluate the paint appearance [31].

[![Watch the video](https://img.youtube.com/vi/tig6Rb4g9aI/hqdefault.jpg)](https://youtu.be/tig6Rb4g9aI)

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
