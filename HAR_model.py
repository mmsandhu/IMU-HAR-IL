import pandas as pd
import numpy as np
import os
import glob

from scipy.stats import skew, kurtosis
from scipy.signal import welch

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# =========================================================
# PARAMETERS
# =========================================================

SAMPLING_RATE = 60              # Hz
WINDOW_SEC = 3                  # seconds
WINDOW_SIZE = SAMPLING_RATE * WINDOW_SEC   # 180 samples
OVERLAP = 0.5
STEP_SIZE = int(WINDOW_SIZE * (1 - OVERLAP))

# =========================================================
# DATASET PATH
# =========================================================

dataset_path = path

# =========================================================
# REPETITIONS
# =========================================================

repetitions = [
    'Repetition_1'
    'Repetition_2',
    'Repetition_3'
    # 'Repetition_4'
]

# =========================================================
# ACTIVITIES
# =========================================================

activities = [
    'Sit',
    'Stand',
    'Walk',
    'Lay',
    'Stairs',
    'Sit_stand',
    'Lay_sit',
    'Wash_face',
    'Brush_teeth',
    'Use_toilet',
    'Shower',
    'Dressing_1',
    'Prepare_meal',
    'Drink',
    'Eat',
    'Kitchen_bin',
    'Medicine'
]

# =========================================================
# AREA LABELS
# =========================================================

area_mapping = {}


for i in range(7):
    area_mapping[activities[i]] = 'Area_1'

for i in range(7, 12):
    area_mapping[activities[i]] = 'Area_2'

for i in range(12, 16):
    area_mapping[activities[i]] = 'Area_3'

area_mapping[activities[16]] = 'Area_4'

# =========================================================
# SENSOR FILES
# =========================================================

files = [
    'bedroom_bed',
    'bedroom_glass',
    'bedroom_hanger',
    'bedroom_med',
    'Body-LLG',
    'Body-LSH',
    'Body-LTH',
    'Body-LUA',
    'Body-LW',
    'Body-RLG',
    'Body-RSH',
    'Body-RTH',
    'Body-RUA',
    'Body-RW',
    'Body-WT',
    'kitchen_bin',
    'kitchen_chair',
    'kitchen_glass',
    'kitchen_jam',
    'kitchen_knife',
    'kitchen_plate',
    'kitchen_table',
    'kitchen_tap',
    'kitchen_toaster',
    'toilet_brush',
    'toilet_facewash',
    'toilet_paste',
    'toilet_seat',
    'toilet_shower',
    'toilet_tap'
]



# =========================================================
# FIND PARTICIPANTS
# =========================================================

participant_days = sorted(
    glob.glob(
        os.path.join(
            dataset_path,
            'Day_*_2024-*'

        )
    )
)

# =========================================================
# FEATURE EXTRACTION FUNCTION
# =========================================================

def extract_features(signal):

    features = []

    # -----------------------------------------------------
    # TIME DOMAIN FEATURES
    # -----------------------------------------------------

    features.append(np.mean(signal))                 # Mean
    features.append(np.std(signal))                  # Std
    features.append(np.var(signal))                  # Variance
    features.append(np.min(signal))                  # Min
    features.append(np.max(signal))                  # Max
    features.append(np.median(signal))               # Median
    features.append(np.ptp(signal))                  # Peak-to-peak
    features.append(np.sqrt(np.mean(signal**2)))     # RMS
    features.append(skew(signal))                    # Skewness
    features.append(kurtosis(signal))                # Kurtosis

    # Zero Crossing Rate
    zcr = np.sum(np.diff(np.sign(signal)) != 0)
    features.append(zcr)

    # Mean Absolute Deviation
    mad = np.mean(np.abs(signal - np.mean(signal)))
    features.append(mad)

    # Signal Energy
    energy = np.sum(signal**2)
    features.append(energy)

    # Entropy
    hist, _ = np.histogram(signal, bins=20)
    hist = hist / np.sum(hist)

    entropy = -np.sum(
        hist * np.log2(hist + 1e-12)
    )

    features.append(entropy)

    # -----------------------------------------------------
    # FREQUENCY DOMAIN FEATURES
    # -----------------------------------------------------

    freqs, psd = welch(
        signal,
        fs=SAMPLING_RATE
    )

    # Dominant Frequency
    dominant_freq = freqs[np.argmax(psd)]
    features.append(dominant_freq)

    # Spectral Energy
    spectral_energy = np.sum(psd)
    features.append(spectral_energy)

    # Spectral Entropy
    psd_norm = psd / np.sum(psd)

    spectral_entropy = -np.sum(
        psd_norm * np.log2(psd_norm + 1e-12)
    )

    features.append(spectral_entropy)

    # Mean Frequency
    mean_freq = np.sum(freqs * psd) / np.sum(psd)
    features.append(mean_freq)

    # Spectral Centroid
    spectral_centroid = mean_freq
    features.append(spectral_centroid)

    return features

# =========================================================
# STORE FEATURES
# =========================================================

X_features = []

y_activity = []

y_area = []

# =========================================================
# PROCESS DATA
# =========================================================

for activity in activities:

    print(f'\nProcessing: {activity}')

    for participant_day in participant_days:

        participant_name = os.path.basename(
            participant_day
        )

        imu_folder = (
            participant_name.split('_2024')[0]
            + '_IMU'
        )

        imu_base_path = os.path.join(
            participant_day,
            imu_folder
        )

        for rep in repetitions:

            activity_path = os.path.join(
                imu_base_path,
                rep,
                activity
            )

            # -------------------------------------------------
            # CHECK FOLDER
            # -------------------------------------------------

            if not os.path.exists(activity_path):
                continue

            available_csvs = [
                f for f in os.listdir(activity_path)
                if f.endswith('.csv')
            ]

            if len(available_csvs) < 30:
                continue

            # -------------------------------------------------
            # LOAD SENSOR DATA
            # -------------------------------------------------

            sensor_dataframes = []

            for file in files:

                file_path = os.path.join(
                    activity_path,
                    f'{file}.csv'
                )

                df = pd.read_csv(file_path)

                # Remove Activity_label column
                if 'Activity_label' in df.columns:
                    df = df.drop(
                        columns=['Activity_label']
                    )

                # Keep first 9-axis columns
                df = df.iloc[:, :9]

                # Rename columns
                df.columns = [
                    f'{file}_{col}'
                    for col in df.columns
                ]

                sensor_dataframes.append(df)

            # -------------------------------------------------
            # MATCH MINIMUM ROWS
            # -------------------------------------------------

            min_rows = min(
                len(df)
                for df in sensor_dataframes
            )

            sensor_dataframes = [
                df.iloc[:min_rows].reset_index(drop=True)
                for df in sensor_dataframes
            ]

            # -------------------------------------------------
            # COMBINE 30 CSV FILES
            # -------------------------------------------------

            combined_df = pd.concat(
                sensor_dataframes,
                axis=1
            )

            combined_df = combined_df.fillna(0, inplace=True)
            # -------------------------------------------------
            # WINDOWING
            # -------------------------------------------------

            for start in range(
                0,
                len(combined_df) - WINDOW_SIZE,
                STEP_SIZE
            ):

                end = start + WINDOW_SIZE

                window = combined_df.iloc[start:end]

                window_features = []

                # ---------------------------------------------
                # EXTRACT FEATURES FROM EACH CHANNEL
                # ---------------------------------------------

                for column in window.columns:

                    signal = window[column].values

                    feats = extract_features(signal)

                    window_features.extend(feats)

                # Store features
                X_features.append(window_features)

                y_activity.append(activity)

                y_area.append(
                    area_mapping[activity]
                )

# =========================================================
# CONVERT TO DATAFRAME
# =========================================================

X_features = pd.DataFrame(X_features)

print("\nFeature Matrix Shape:")
print(X_features.shape)

# =========================================================
# ENCODE LABELS
# =========================================================

activity_encoder = LabelEncoder()

y_activity_encoded = activity_encoder.fit_transform(
    y_activity
)

area_encoder = LabelEncoder()

y_area_encoded = area_encoder.fit_transform(
    y_area
)

# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train_act, X_test_act, y_train_act, y_test_act = (
    train_test_split(
        X_features,
        y_activity_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_activity_encoded
    )
)

X_train_area, X_test_area, y_train_area, y_test_area = (
    train_test_split(
        X_features,
        y_area_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_area_encoded
    )
)

# =========================================================
# RANDOM FOREST:
# 18 ACTIVITY RECOGNITION
# =========================================================

activity_rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Activity RF Model...")

activity_rf.fit(
    X_train_act,
    y_train_act
)

# =========================================================
# EVALUATION
# =========================================================

y_pred_act = activity_rf.predict(
    X_test_act
)

activity_accuracy = accuracy_score(
    y_test_act,
    y_pred_act
)

activity_f1 = f1_score(
    y_test_act,
    y_pred_act,
    average='weighted'
)

print("\n================================")
print("18 Activity Recognition Results")
print("================================")

print(f'Accuracy : {activity_accuracy:.4f}')
print(f'F1-Score : {activity_f1:.4f}')

# =========================================================
# RANDOM FOREST:
# 4 AREA RECOGNITION
# =========================================================

area_rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Area RF Model...")

area_rf.fit(
    X_train_area,
    y_train_area
)

# =========================================================
# EVALUATE AREA MODEL
# =========================================================

y_pred_area = area_rf.predict(
    X_test_area
)

area_accuracy = accuracy_score(
    y_test_area,
    y_pred_area
)

area_f1 = f1_score(
    y_test_area,
    y_pred_area,
    average='weighted'
)

print("\n==============================")
print("4 Area Recognition Results")
print("==============================")

print(f'Accuracy : {area_accuracy:.4f}')
print(f'F1-Score : {area_f1:.4f}')
