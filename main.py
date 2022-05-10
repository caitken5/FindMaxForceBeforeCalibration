# I want to know the raw measured values of the force sensor along the x, y, and z axes, in addition to the torque about
# the z axis. This means I don't want values that have been converted to the global frame of the device. Therefore I
# will start with the files stored in LLR_DATA_NPY_FILES.

# The goal of this code is to identify the distribution of forces in stored in each of the files to better indicate
# how the sensor should be calibrated.

# Reminder of the structure of the OptoForce files:
# - Sequential data points are stored in a new column at each time stamp.
# - Data in the rows are stored in the following sequence:
# 1. Time, starting from 0, recorded at 1000 Hz.
# 2. Magnitude of force along the x-axis.
# 3. Magnitude of force along the y-axis.
# 4. Magnitude of force along the z-axis.
# 5. Magnitude of torque about the x-axis.
# 6. Magnitude of torque about the y-axis.
# 7. Magnitude of torque about the z-axis.

# Crucial rows of data are 2, 3, and 7. Row 4 will also be measured as a mental note.

# For each of these 4 pieces of data, the minimum, maximum, mean, median, and standard deviation values of force and \
# torque will be recorded. This data will be stored in the following manner:
# - Rows will correspond to a new loaded file.
# - Columns will correspond to the stored data, as follows:
# 1. Fx Minimum. 2. Fx Maximum. 3. Fx Mean. 4. Fx Median. 5. Fx std dev.
# 6. Fy Minimum. 7. Fy Maximum. 8. Fy Mean. 9. Fy Median. 10. Fy std dev.
# 11. Tz Minimum. 12. Tz Maximum. 13. Tz Mean. 14. Tz Median. 15. Tz std dev.
# 16. Fz Minimum. 17. Fz Maximum. 18. Fz Mean. 19. Fz Median. 20. Fz std dev.

# Import necessary libraries
import os
import numpy as np
import pandas as pd


# Cute little function here for finding the min, max, mean, median, and std dev for each of the f/t values.
def get_force_char(row_of_data):
    if row_of_data.ndim:
        # Here if the data has not been reformatted to two dimensions.
        row_of_data = row_of_data.reshape((1, -1))  # Reshapes data to two dimensions where the row has a value of 1.
    minimum = np.min(row_of_data)
    maximum = np.max(row_of_data)
    mean = np.mean(np.abs(row_of_data))
    median = np.median(np.abs(row_of_data))
    std = np.std(np.abs(row_of_data))
    return np.asarray([minimum, maximum, mean, median, std])


load_path = 'D:/PD_Participant_Data/LLR_DATA_ANALYSIS_CLEANED/LLR_DATA_NPY_FILES/'
# load_path = 'G:/PD_Participant_Data/LLR_DATA_ANALYSIS_CLEANED/LLR_DATA_NPY_FILES'
save_path = 'D:/PD_Participant_Data/LLR_DATA_ANALYSIS_CLEANED/UNCALIBRATED_ABSOLUTE_FORCE_STATISTICS.CSV'
columns = ["Fx_min", "Fx_max", "Fx_mean", "Fx_median", "Fx_std", "Fy_min", "Fy_max", "Fy_mean", "Fy_median", "Fy_std",
           "Tz_min", "Tz_max", "Tz_mean", "Tz_median", "Tz_std", "Fz_min", "Fz_max", "Fz_mean", "Fz_median", "Fz_std"]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Finding the maximum force measured by the force sensor for all data collected so far to estimate forces "
          "required for calibration process.")
    print("This code is not a standard part of the LLR data process. This is used to identify the range of forces "
          "typically applied to the robot for calibration testing of the OptoForce sensor on the LLR.")

    # Start of the meat of the code. Initialize an empty array to store the data with 20 columns and the number of rows
    # equal to the number of files being read.
    count = 0
    for file in os.listdir(load_path):
        if ("OptoForce" in file) and (file.endswith('.npy')):
            count += 1
    # Let force_char be the array that holds the data outlined in the introduction of this code.
    force_char = np.zeros((count, 20), dtype='float64')
    # Cycle through the files that have been converted to numpy from .mat files.
    i = 0  # For counting through the rows in the force_char array as files are loaded.
    for file in os.listdir(load_path):
        if ("OptoForce" in file) and (file.endswith('.npy')):
            # I only want to load the OptoForce files for the testing of the OptoForce sensor.
            load_file = load_path + file
            # Load the data into the workspace.
            force_array = np.load(load_file)
            # Collect the necessary information from each of the rows.
            force_char[i, 0:5] = get_force_char(force_array[1, :])  # Fx.
            force_char[i, 5:10] = get_force_char(force_array[2, :])  # Fy.
            force_char[i, 10:15] = get_force_char(force_array[6, :])  # Tz.
            force_char[i, 15:] = get_force_char(force_array[3, :])  # Fz.
            i += 1
        if i % 10 == 0:
            print(str(i), " of ", str(count), "...")
    # Save all of the collected data to a csv file.
    df = pd.DataFrame(force_char, columns=columns)
    df.to_csv(save_path)
    # Close the program.
    print("FindMaxForceBeforeCalibration Code done running. See results in optoforce_characteristics.csv")
