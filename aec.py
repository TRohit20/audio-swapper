import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import librosa
import soundfile as sf
import time

def create_audio_signal(duration=3, sample_rate=22050):
    """Create a simple audio signal."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Create a signal with multiple frequencies
    return 0.5 * np.sin(2 * np.pi * 440 * t) + 0.3 * np.sin(2 * np.pi * 880 * t)

def add_echo(audio, delay_samples=2000, decay=0.6):
    """Add an echo effect to the audio signal."""
    echo = np.zeros_like(audio)
    echo[delay_samples:] = audio[:-delay_samples] * decay
    return audio + echo

def apply_acoustic_echo_cancellation(mixed_signal, reference_signal, filter_length=1000):
    """Simple implementation of acoustic echo cancellation using adaptive filtering."""
    # Initialize filter coefficients
    filter_coeffs = np.zeros(filter_length)
    # Learning rate
    mu = 0.01
    
    cancelled_signal = np.zeros_like(mixed_signal)
    
    # Process the signal sample by sample
    for n in range(len(mixed_signal) - filter_length):
        # Get the current chunk of the reference signal
        x = reference_signal[n:n + filter_length]
        
        # Estimate echo
        echo_estimate = np.dot(filter_coeffs, x)
        
        # Calculate error
        error = mixed_signal[n] - echo_estimate
        
        # Update filter coefficients using LMS algorithm
        filter_coeffs = filter_coeffs + mu * error * x
        
        # Store the processed sample
        cancelled_signal[n] = error
    
    return cancelled_signal

def plot_waveform(signal, title, color='blue'):
    """Plot a waveform with a given title and color."""
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.plot(signal[:1000], color=color)
    ax.set_title(title)
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    return fig

def main():
    st.title("Acoustic Echo Cancellation Demo")
    st.write("""
    This app demonstrates how Acoustic Echo Cancellation (AEC) works in modern communication systems.
    Watch how the system removes unwanted echo from the audio signal!
    """)
    
    # Sidebar controls
    st.sidebar.header("Signal Parameters")
    duration = st.sidebar.slider("Signal Duration (seconds)", 1, 5, 3)
    echo_delay = st.sidebar.slider("Echo Delay (ms)", 50, 500, 100)
    echo_strength = st.sidebar.slider("Echo Strength", 0.1, 0.9, 0.6)
    
    # Create signals when user clicks button
    if st.button("Generate New Signals"):
        # Progress bar
        progress_bar = st.progress(0)
        
        # Original signal (simulating the remote speaker's voice)
        original_signal = create_audio_signal(duration=duration)
        progress_bar.progress(25)
        
        # Add echo to simulate room acoustics
        echo_samples = int(echo_delay * 22.05)  # Convert ms to samples
        mixed_signal = add_echo(original_signal, echo_samples, echo_strength)
        progress_bar.progress(50)
        
        # Apply echo cancellation
        cleaned_signal = apply_acoustic_echo_cancellation(mixed_signal, original_signal)
        progress_bar.progress(75)
        
        # Plotting
        st.subheader("Signal Visualization")
        
        # Original signal plot
        st.write("Original Signal (Remote Speaker)")
        st.pyplot(plot_waveform(original_signal, "Original Signal", 'blue'))
        
        # Mixed signal plot
        st.write("Mixed Signal (With Echo)")
        st.pyplot(plot_waveform(mixed_signal, "Mixed Signal (Voice + Echo)", 'red'))
        
        # Cleaned signal plot
        st.write("Cleaned Signal (After Echo Cancellation)")
        st.pyplot(plot_waveform(cleaned_signal, "Cleaned Signal", 'green'))
        
        progress_bar.progress(100)
        time.sleep(0.5)
        progress_bar.empty()
        
        # Explanation
        st.subheader("What's happening here?")
        st.write("""
        1. **Original Signal** (Blue): This represents the audio coming from the remote speaker.
        
        2. **Mixed Signal** (Red): This shows what your microphone would capture - a mixture of the original signal plus its echo.
        The echo is created when the speaker output bounces around your room before reaching the microphone.
        
        3. **Cleaned Signal** (Green): This is the result after applying Acoustic Echo Cancellation.
        The algorithm knows what was played through the speakers and uses this information to remove the echo from the microphone input.
        
        Try adjusting the echo delay and strength in the sidebar to see how different room conditions affect the signal!
        """)

if __name__ == "__main__":
    main()