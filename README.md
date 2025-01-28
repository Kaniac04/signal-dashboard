# Signal Processing Dashboard

This is a **Streamlit-based Signal Processing Dashboard** that allows users to process and analyze accelerometer data and GPS location data from two uploaded CSV files. The app includes functionalities for preprocessing, applying a low-pass filter to signals, and visualizing filtered signals.

## Features

1. **CSV File Upload**: Upload two CSV files for analysis.
   - `Location.csv`: Contains GPS data (latitude, longitude, and time).
   - `Accelerometer.csv`: Contains accelerometer readings (x, y, z values and time).
2. **Preprocessing**: View a detailed summary of the uploaded data in a user-friendly interface.
   - Displays the first few rows of each file.
   - Shows the shape and column data types of the data.
3. **Low-Pass Filter**:
   - Configure the sampling rate, cutoff frequency, and filter order.
   - Apply the filter to the accelerometer signals (x, y, z) and visualize the results.
4. **Interactive Visualization**: View filtered signals as line plots for easy analysis.
5. **Dark Theme**: Clean, professional UI with a dark theme.

## Test the APP


## Input File Requirements

The application requires two specific CSV files:

### 1. **Location.csv**

This file must contain the following columns:

- `seconds_elapsed`: Time in seconds since the start of data collection.
- `latitude`: Latitude coordinate.
- `longitude`: Longitude coordinate.

### 2. **Accelerometer.csv**

This file must contain the following columns:

- `seconds_elapsed`: Time in seconds since the start of data collection.
- `x`: Acceleration in the x-axis.
- `y`: Acceleration in the y-axis.
- `z`: Acceleration in the z-axis.

Ensure that both files share a common `seconds_elapsed` column to align the data for analysis.

## How to Run the Application

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies** Ensure you have Python 3.8 or later installed. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application** Start the Streamlit app using the following command:

   ```bash
   streamlit run app.py
   ```

4. **Open the Application** After running the command, Streamlit will provide a local URL (e.g., `http://localhost:8501/`). Open this URL in your web browser to access the dashboard.

## How to Use the Application

1. **Upload Files**:

   - Use the sidebar to upload the `Location.csv` and `Accelerometer.csv` files.

2. **Pre-process Data**:

   - Click the "Pre-process and Display DataFrame Info" button to view the summary of the uploaded data, including the first 10 rows, shape, and column data types.

3. **Configure Filter Parameters**:

   - Set the following parameters in the sidebar:
     - Sampling Rate (Hz)
     - Cutoff Frequency (Hz)
     - Order of the Low-Pass Filter

4. **Apply Low-Pass Filter**:

   - Click the "Apply Low Pass Filter and Plot" button to filter the accelerometer data and visualize the filtered signals.

## Example Output

- **Pre-Processed Data**: Interactive tables showing data summaries for both `Location.csv` and `Accelerometer.csv`.
- **Filtered Signals**: Line plots of accelerometer data (x, y, z) before and after applying the low-pass filter.

## Dependencies

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- SciPy
- Matplotlib

## Folder Structure

```
project-folder/
├── app.py                # Main application script
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
```

## Notes

- Make sure the `seconds_elapsed` column in both files is aligned for accurate filtering and plotting.
- Test the application with sample data to ensure it meets your requirements.


