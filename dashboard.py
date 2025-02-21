import streamlit as st
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import plotly.graph_objects as go
import pydeck as pdk

# Configure the page
st.set_page_config(page_title="Signal Processing Dashboard", layout="wide", page_icon="🌐")

st.markdown("""
    <style>
    body {
        color: #fff;
        background-color: #121212;
    }
    .stButton>button {
        background-color: #333;
        color: white;
    }
    .stNumberInput>div>div>input {
        color: white;
        background-color: #333;
    }
    </style>
""", unsafe_allow_html=True)

class SignalProcessingApp:
    def __init__(self):
        self.file1 = None
        self.file2 = None
        self.sampling_rate = 10
        self.cutoff_freq = 2.0
        self.filter_order = 2
        self.calibration_buffer = 5

    def sidebar_inputs(self):
        st.sidebar.title("Signal Processing Inputs")
        st.sidebar.markdown("### File Inputs")
        
        # File uploads
        self.file1 = st.sidebar.file_uploader("Upload the Location CSV file", type="csv")
        self.file2 = st.sidebar.file_uploader("Upload the Accelerometer CSV file", type="csv")

        # Numerical inputs
        self.sampling_rate = st.sidebar.number_input("Sampling Rate (Hz)", min_value=1, value=10, step=1)
        self.cutoff_freq = st.sidebar.number_input("Cutoff Frequency (Hz)", min_value=0.1, value=2.0, step=0.1, format="%.2f")
        self.filter_order = st.sidebar.number_input("Order of Low Pass Filter", min_value=1, value=2, step=1)

    def display_dataframe_info(self):
        if self.file1 and self.file2:
            try:
                df1 = pd.read_csv(self.file1,usecols=lambda column: column != 'time')
                df2 = pd.read_csv(self.file2,usecols=lambda column: column != 'time')

                dashboard_col_1, dashboard_col_2 = st.columns(2)

                with dashboard_col_1:
                    st.write("### Info of Location DataFrame")
                    st.dataframe(df1.head(10))  # Display the first few rows
                    st.markdown("**Shape:**")
                    st.write(df1.shape)
                    st.markdown("**Column Details:**")
                    st.table(df1.dtypes.rename("Data Type").to_frame())

                with dashboard_col_2:
                    st.write("### Info of Accelerometer DataFrame")
                    st.dataframe(df2.head(10))  # Display the first few rows
                    st.markdown("**Shape:**")
                    st.write(df2.shape)
                    st.markdown("**Column Details:**")
                    st.table(df2.dtypes.rename("Data Type").to_frame())

            except Exception as e:
                st.error(f"Error processing files: {e}")
        else:
            st.error("Please upload both CSV files.")

    def low_pass_filter(self, data, cutoff, fs, order):
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, data)
        return y

    def preprocess_data(self,df1 : pd.DataFrame, df2 : pd.DataFrame) -> pd.DataFrame:
        df1["timestamp_int"] = df1["seconds_elapsed"].apply(lambda x : int(x))
        df2["timestamp_int"] = df2["seconds_elapsed"].apply(lambda x : int(x) )
        df2["inclusion"] = df2["timestamp_int"].apply(lambda x : True if x >=self.calibration_buffer else False)
        df2 = df2[df2["inclusion"]]
        combined_Data = pd.merge(df2, df1, on="timestamp_int",how="left")
        combined_Data = combined_Data.iloc[:,[1,2,3,4,5,16,17]]

        combined_Data["filtered_y"] = self.low_pass_filter(combined_Data['y'],self.cutoff_freq,self.sampling_rate,self.filter_order)

        return combined_Data

    def plot_sensor_data(self, combined_Data : pd.DataFrame):

        st.write("### Info of Pre-processed Combined DataFrame")
        st.dataframe(combined_Data.head(10))  # Display the first few rows
        st.markdown("**Shape:**")
        st.write(combined_Data.shape)
        st.markdown("**Column Details:**")
        st.table(combined_Data.dtypes.rename("Data Type").to_frame())

        fig = go.Figure()

        # Add the original data
        fig.add_trace(go.Scatter(
            x=combined_Data['seconds_elapsed_x'],
            y=combined_Data['y'],
            mode='lines',
            name='Original',
            line=dict(color='blue')
        ))

        # Add the Low-Pass Filtered data
        fig.add_trace(go.Scatter(
            x=combined_Data['seconds_elapsed_x'],
            y=combined_Data['filtered_y'],
            mode='lines',
            name='LPF Filtered',
            line=dict(color='orange')
        ))

        # Customize the layout
        fig.update_layout(
            title='Interactive Sensor Data Visualization',
            xaxis_title='Timestamp (seconds_elapsed)',
            yaxis_title='Sensor Reading (y)',
            legend_title='Data Type',
            hovermode='x unified',
            template="plotly_dark",
            legend=dict(x=0, y=1),
            margin=dict(l=40, r=40, t=40, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Interactive GPS Map")
        combined_Data = combined_Data.reset_index()

        # Define the Pydeck Layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=combined_Data,
            get_position=["longitude", "latitude"],
            get_radius=2,  # Adjust point size
            get_color=[255, 0, 0, 160],  # Red points
            pickable=True,
            auto_highlight = True
        )

        tooltip = { 
        "html": "<b>X:</b> {x} <br/> <b>Y:</b> {y} <br/> <b>Z:</b> {z} <br/> <b>Latitude:</b> {latitude} <br/> <b>Longitude:</b> {longitude} <br/> <b>Seconds Elapsed:</b> {seconds_elapsed_x}",
        "style": {"backgroundColor": "black", "color": "white"},
        }

        view_state = pdk.data_utils.compute_view(combined_Data[["longitude", "latitude"]])
        view_state.pitch = 0  # Keep the map flat


        # Render the map
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))

    def apply_filter_and_plot(self):
        if self.file1 and self.file2:
            try:
                df1 = pd.read_csv(self.file1)
                df2 = pd.read_csv(self.file2)

                if 'seconds_elapsed' not in df1.columns or len(df1.columns) < 2:
                    st.error("Location data must be time-series data or there is an error in data-structure.")
                elif 'seconds_elapsed' not in df2.columns or len(df2.columns) < 2:
                    st.error("Accelerometer data must be time-series data or there is an error in data-structure.")
                else:
                    combined_Data = self.preprocess_data(df1,df2)
                    self.plot_sensor_data(combined_Data=combined_Data)

            except Exception as e:
                st.error(f"Error processing files: {e}")
        else:
            st.error("Please upload both CSV files.")

    def run(self):
        self.sidebar_inputs()

        if st.sidebar.button("Pre-process and Display DataFrame Info"):
            self.display_dataframe_info()

        if st.sidebar.button("Apply Low Pass Filter and Plot Maps"):
            self.apply_filter_and_plot()

if __name__ == "__main__":
    app = SignalProcessingApp()
    app.run()
