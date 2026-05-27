# IMU-HAR-IL Dataset
This is IMU sensor dataset for Human Activity Recognition (HAR) to support Independednt Living (IL) in smart homes. <br>

**Data Collection**

**Sensors Used:**

Xsens DOT (https://www.xsens.com/wearables/xsens-dot)

All data stored at **60 Hz.**

**Sensor deployment:** 11 ob body and 19 on different objects in the home

**Collection Period:** From June 2024 to Sep 2024

**Environment:** 1-bed residential unit

**Collection Protocol:** Data collected from 50 adult participants.
Ethics approval to complete this study was obtained from CSIRO's Health and Medical Human Research Ethics Committee, before conducting this study (Approval number: 2024_018_LR). All participants provided informed written consent before participating in the study.

Dataset Structure:

**The data is organised in 50 folders (for 50 participants):**


P01
P02
.
.
P50


**Each folder has 3-4 subfolders (for each repetition):**


Repetition_1
Repetition_2
Repetition_3
Repetition_4


Each subfolder contains 18 subfolders corresponding to each activity.

Brush_teeth
Dressing_1
Dressing_2
Drink
Eat
Kitchen_bin
Lay
Lay_sit
Medicine
Prepare_meal
Shower
Sit
Sit_stand
Stairs
Stand
Use_toilet
Walk
Wash_face

Each subfolder contains 30 CSV files containing data from 30 IMU sensors (11 on the body and 19 on various objects in the home).

bedroom_bed.csv
bedroom_glass.csv
bedroom_hanger.csv
bedroom_med.csv
Body-LLG.csv
Body-LSH.csv
Body-LTH.csv
Body-LUA.csv
Body-LW.csv
Body-RLG.csv
Body-RSH.csv
Body-RTH.csv
Body-RUA.csv
Body-RW.csv
Body-WT.csv
kitchen_bin.csv
kitchen_chair.csv
kitchen_glass.csv
kitchen_jam.csv
kitchen_knife.csv
kitchen_plate.csv
kitchen_table.csv
kitchen_tap.csv
kitchen_toaster.csv
toilet_brush.csv
toilet_facewash.csv
toilet_paste.csv
toilet_seat.csv
toilet_shower.csv
toilet_tap.csv

**File Formats:** CSV for time-series data
IMU data:
`Euler_X`, `Euler_Y`, `Euler_Z`: 3D orientation 
`Acc_X`, `Acc_Y`, `Acc_Z`: 3D acceleration 
`Gyr_X`, `Gyr_Y`, `Gyr_Z`: Angular velocity around the three spatial axes—pitch, roll, and yaw.
`Activity_label`: A unique number to identify the activity.

**Raw Data Status:** This is raw data segmented into 18 activities (break period were removed).

**Preprocessing Steps:**

**Segmentation:** Data was segmented into 5 activities and break periods were removed.



**Link to Data:**

https://doi.org/10.25919/85j1-6z03 


**Please cite the relevant work.**

1- Moid Sandhu, et al. "Feasibility of motion sensor-based human activity recognition for supporting independence in smart homes." Maturitas 199 (2025): 108632. https://www.sciencedirect.com/science/article/pii/S0378512225004402 

2- Moid Sandhu, et al. "Fusing IoT Wearable and Object Motion Sensors for Enhanced Activity Recognition in Smart Homes." 2025 47th Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC). IEEE, 2025. https://ieeexplore.ieee.org/abstract/document/11253505/ 

