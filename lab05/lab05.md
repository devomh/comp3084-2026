# Lab 05: Digital Waves -- Lab Notebook
**Audio Forensics & Signal Manipulation with NumPy Arrays**

---

## Introduction

Welcome to the Audio Forensics Division. You have been assigned the role of **Audio Forensics Analyst** on a sensitive case. A recording recovered from a seized laptop (`mystery.wav`) appears to contain only static noise. Intelligence suggests the original message was **reversed** and **buried under a synthetic hum** to prevent casual listening.

Your mission is threefold:

1. **Understand** how digital audio is represented as a NumPy array.
2. **Build** a custom audio manipulation toolkit using only raw array mathematics.
3. **Recover** a hidden spoken message by combining noise cancellation, reversal, and volume boosting.

**Constraints:** You may use `scipy.io.wavfile` only for loading and saving WAV files. You may use Matplotlib for visualization and `IPython.display.Audio` for playback. All audio processing must be implemented with raw NumPy array operations. No `librosa`, `pydub`, `soundfile`, or `scipy.signal`.

**Reference:** Consult [`concepts.md`](concepts.md) for detailed background on sound representation, int16 arithmetic, waveform visualization, and how every audio effect maps to a Precalculus function transformation.

---

## Setup

Run this cell first to import all required libraries.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from IPython.display import Audio, display
```

---

## Phase 1: The Sound as a List (30 min)

Before we can analyze forensic recordings, we need to understand how a computer represents sound. At its core, every digital audio file is a **list of numbers** — each number records the air pressure at one instant in time. A microphone captures these measurements many thousands of times per second, and a WAV file stores them as a NumPy array.

---

### Exercise 1.1: Loading a WAV File

Our first task is to load an audio file into memory and inspect its structure. Scipy's `wavfile.read()` handles the WAV binary header and returns the raw sample data as a NumPy array.

```python
# Load the stereo test sample
rate, data = wavfile.read('data/stereo_sample.wav')

# Inspect the array structure
print(f"Sample Rate: {rate} Hz")
print(f"Shape: {data.shape}")
print(f"Dtype: {data.dtype}")
print(f"Duration: {len(data) / rate:.2f} seconds")
print(f"Min: {data.min()}, Max: {data.max()}")
print(f"First 5 samples: {data[:5]}")
```

<details>
<summary>Expected Output</summary>

```
Sample Rate: 16000 Hz
Shape: (64000, 2)
Dtype: int16
Duration: 4.00 seconds
Min: -20000, Max: 20000
First 5 samples: [[   0    0]
 [...]
```

The shape `(64000, 2)` tells us there are 64,000 samples and 2 channels (stereo). The dtype `int16` means signed 16-bit integers (range -32,768 to +32,767). The sample rate of 16,000 Hz means 16,000 measurements per second.
</details>

**Task:** Load `pure_hum.wav` and inspect its properties. Is it mono or stereo? What is its sample rate and duration?

```python
# TODO: Load pure_hum.wav and inspect its properties
rate_h, hum = wavfile.read('data/pure_hum.wav')
print(f"Sample Rate: {rate_h} Hz")
print(f"Shape: {hum.shape}")
print(f"Dtype: {hum.dtype}")
print(f"Duration: {len(hum) / rate_h:.2f} seconds")
print(f"Min: {hum.min()}, Max: {hum.max()}")
```

---

### Exercise 1.2: Visualizing the Waveform

Numbers alone do not tell the whole story. We need to *see* the sound. A **waveform plot** shows amplitude (y-axis) vs. time in seconds (x-axis).

```python
# Full waveform view (use left channel of stereo data)
left_channel = data[:, 0]
time_axis = np.arange(len(left_channel)) / rate

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(time_axis, left_channel, linewidth=0.5, color='steelblue')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude')
ax.set_title('Waveform: stereo_sample.wav (Left Channel)')
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()
```

**Zoomed View:** To see individual wave oscillations, plot only a small window (10 milliseconds):

```python
window = int(0.01 * rate)  # 10ms worth of samples
t_window = np.arange(window) / rate * 1000  # Convert to milliseconds

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(t_window, left_channel[:window], linewidth=1.0, color='steelblue',
        marker='.', markersize=4)
ax.set_xlabel('Time (milliseconds)')
ax.set_ylabel('Amplitude')
ax.set_title('Zoomed View: First 10 ms')
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()
```

**Question:** What does a single "wave" look like up close? Why do the dots form a smooth curve even though they are discrete sample points?

---

### Exercise 1.3: Listening to the Audio

Waveform plots show us the *shape* of the sound, but we also need to *hear* it. `IPython.display.Audio` renders an HTML5 audio player directly in the notebook.

```python
# For stereo data, Audio expects shape (channels, N) — so transpose
print("Stereo sample:")
display(Audio(data=data.T, rate=rate))
```

**Convention (IMPORTANT):** From this point on, every transformation follows the **See-Then-Hear** pattern:

1. **Transform** the audio
2. **See** — plot the waveform
3. **Hear** — play the audio

This dual verification is critical. A waveform might *look* correct but sound wrong (or vice versa). Always verify both ways.

---

### Exercise 1.4: Stereo-to-Mono Conversion

Stereo audio has two channels (left and right). For simplicity, all our processing will work on **mono** (single-channel) audio. To convert, we average the two channels.

**The Math:** `mono[i] = (left[i] + right[i]) / 2`

```python
def to_mono(data):
    """Convert stereo audio to mono by averaging channels.

    Args:
        data: NumPy array of shape (N, 2), dtype int16

    Returns:
        NumPy array of shape (N,), dtype int16
    """
    if data.ndim == 1:
        return data  # Already mono
    # TODO: Average both channels. Use float64 to avoid overflow, then cast back.
    # Hint: data[:, 0] is the left channel, data[:, 1] is the right channel
    pass
```

```python
# Test: convert stereo sample to mono
mono = to_mono(data)
print(f"Original shape: {data.shape}")
print(f"Mono shape: {mono.shape}")
print(f"Dtype: {mono.dtype}")
```

<details>
<summary>Expected Output</summary>

```
Original shape: (64000, 2)
Mono shape: (64000,)
Dtype: int16
```
</details>

```python
# See-Then-Hear: compare stereo vs mono
fig, axes = plt.subplots(2, 1, figsize=(12, 5), sharex=True)
time_axis = np.arange(len(mono)) / rate

axes[0].plot(time_axis, data[:, 0], linewidth=0.5, color='steelblue')
axes[0].set_title('Left Channel')
axes[0].set_ylabel('Amplitude')
axes[0].axhline(y=0, color='gray', linestyle='--', linewidth=0.5)

axes[1].plot(time_axis, mono, linewidth=0.5, color='green')
axes[1].set_title('Mono (Average of L+R)')
axes[1].set_ylabel('Amplitude')
axes[1].axhline(y=0, color='gray', linestyle='--', linewidth=0.5)

axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
plt.show()

print("Stereo:")
display(Audio(data=data.T, rate=rate))
print("Mono:")
display(Audio(data=mono, rate=rate))
```

From this point forward, we will use the mono version of our test audio. Let's assign it:

```python
# Use mono audio for all subsequent exercises
sample = to_mono(data)
```

---

## Phase 2: The "Anti-Sound" & Volume (45 min)

Now that we can load, visualize, and listen to audio, we move to our first transformations. Each effect maps directly to a **Precalculus function transformation** you already know — see the table in [`concepts.md`](concepts.md).

---

### Part A: Volume Control — Vertical Scaling (15 min)

**Goal:** Adjust the volume of a sound by multiplying every sample by a scalar.

**The Math (Precalculus: Vertical Stretch/Compression):**

```
louder[i]  = factor × sample[i],    where factor > 1   (stretch)
quieter[i] = factor × sample[i],    where 0 < factor < 1 (compression)
```

**Critical Warning — int16 Overflow:**

Just like `uint8` in Lab 04, `int16` arithmetic wraps around silently:

```python
# DANGER: int16 overflow demonstration
a = np.int16(20000)
print(f"int16(20000) * 2 = {a * np.int16(2)}")   # -25536, NOT 40000!
print(f"Expected: {20000 * 2}")                     # 40000

# The fix: always work in float64
result = np.float64(20000) * 2.0
print(f"float64(20000) * 2 = {result}")              # 40000.0
print(f"Clipped: {np.clip(result, -32768, 32767)}")   # 32767.0
```

<details>
<summary>Expected Output</summary>

```
int16(20000) * 2 = -25536
Expected: 40000
float64(20000) * 2 = 40000.0
Clipped: 32767.0
```

The value 40,000 exceeds int16's maximum of 32,767, so it wraps to -25,536. The safe approach: convert to float64, do math, clip, cast back.
</details>

**Implementation:**

```python
def adjust_volume(data, factor):
    """Scale audio volume by a constant factor.

    Args:
        data: NumPy array, dtype int16
        factor: float multiplier (1.0 = no change, 2.0 = double, 0.5 = half)

    Returns:
        NumPy array with same shape, dtype int16
    """
    # TODO: Implement
    # Step 1: Convert to float64 to avoid overflow
    # Step 2: Multiply by factor
    # Step 3: Clip to [-32768, 32767]
    # Step 4: Cast back to int16
    pass
```

```python
# Test volume control
loud = adjust_volume(sample, 2.0)
quiet = adjust_volume(sample, 0.3)

print(f"Original — min: {sample.min()}, max: {sample.max()}")
print(f"Loud (×2) — min: {loud.min()}, max: {loud.max()}")
print(f"Quiet (×0.3) — min: {quiet.min()}, max: {quiet.max()}")
```

<details>
<summary>Expected Output</summary>

```
Original — min: -20000, max: 20000
Loud (×2) — min: -32768, max: 32767       (clipped — would have been ±40000)
Quiet (×0.3) — min: -6000, max: 6000
```

The loud version is clipped at the int16 boundaries because 20000 × 2 = 40000 > 32767.
</details>

```python
# See-Then-Hear: compare all three
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
for ax, signal, title in zip(axes,
    [sample, loud, quiet],
    ['Original', 'Volume × 2.0 (clipped)', 'Volume × 0.3']):
    t = np.arange(len(signal)) / rate
    ax.plot(t, signal, linewidth=0.5, color='steelblue')
    ax.set_title(title)
    ax.set_ylabel('Amplitude')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
plt.show()

print("Original:")
display(Audio(data=sample, rate=rate))
print("Louder (×2.0):")
display(Audio(data=loud, rate=rate))
print("Quieter (×0.3):")
display(Audio(data=quiet, rate=rate))
```

**Question:** What happens if you multiply by 10.0 without clipping? Why does it sound *distorted* rather than just very loud? (Hint: think about what happens when the wave peaks exceed ±32,767.)

---

### Part B: Phase Inversion — The Mirror Wave (10 min)

**Goal:** Multiply the signal by -1 to flip it across the x-axis.

**The Math (Precalculus: Reflection over x-axis):**

```
inverted = -f(x)
```

**Implementation:**

```python
inverted = -sample  # A single NumPy operation!
```

```python
# See-Then-Hear: compare original vs inverted (zoomed to 10ms)
window = int(0.01 * rate)
t_win = np.arange(window) / rate * 1000  # milliseconds

fig, axes = plt.subplots(2, 1, figsize=(12, 5), sharex=True)
axes[0].plot(t_win, sample[:window], color='steelblue', linewidth=1.5)
axes[0].set_title('Original')
axes[1].plot(t_win, inverted[:window], color='crimson', linewidth=1.5)
axes[1].set_title('Phase Inverted (× -1)')
for ax in axes:
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_ylabel('Amplitude')
axes[-1].set_xlabel('Time (milliseconds)')
plt.tight_layout()
plt.show()

print("Original:")
display(Audio(data=sample, rate=rate))
print("Inverted:")
display(Audio(data=inverted, rate=rate))
```

**Discovery:** Listen carefully — they sound *identical*! The graph proves they are different (one is the mirror image of the other), but the human ear perceives amplitude *patterns*, not whether peaks are positive or negative. The waves look completely different but are perceptually indistinguishable.

---

### Part C: Noise Cancellation — Destructive Interference (20 min)

**Goal:** Demonstrate that adding a signal to its inverse produces silence (all zeros), then apply this forensically to remove a hum from a contaminated recording.

**The Math (Precalculus: Additive Inverse):**

```
f(x) + (-f(x)) = 0    for every x
```

**Step 1: Perfect Cancellation Demo**

```python
# Generate a pure sine wave (a "hum")
duration = 2.0
t = np.linspace(0, duration, int(rate * duration), endpoint=False)
hum_demo = np.int16(10000 * np.sin(2 * np.pi * 220 * t))  # 220 Hz

# Create the anti-sound
anti_hum = -hum_demo

# Add them
result = hum_demo.astype(np.int32) + anti_hum.astype(np.int32)

print(f"Sum min: {result.min()}, max: {result.max()}")
print(f"All zeros? {np.all(result == 0)}")
```

<details>
<summary>Expected Output</summary>

```
Sum min: 0, max: 0
All zeros? True
```

Perfect cancellation: every sample in the sum is exactly zero — silence.
</details>

```python
# See-Then-Hear: visualize the cancellation
window = int(0.02 * rate)  # 20ms
t_win = np.arange(window) / rate * 1000

fig, axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)

axes[0].plot(t_win, hum_demo[:window], color='steelblue', linewidth=2)
axes[0].set_title('Signal: 220 Hz Hum')

axes[1].plot(t_win, anti_hum[:window], color='crimson', linewidth=2)
axes[1].set_title('Anti-Signal: -1 × Hum')

axes[2].plot(t_win, result[:window], color='green', linewidth=2)
axes[2].set_title('Sum: Signal + Anti-Signal = Silence')
axes[2].set_ylim(-12000, 12000)

for ax in axes:
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_ylabel('Amplitude')
axes[-1].set_xlabel('Time (milliseconds)')
plt.tight_layout()
plt.show()

print("Hum:")
display(Audio(data=hum_demo, rate=rate))
print("Anti-Hum:")
display(Audio(data=anti_hum, rate=rate))
print("Sum (should be silent):")
display(Audio(data=result.astype(np.int16), rate=rate))
```

**Step 2: Forensic Application — Remove Hum from a Dirty Recording**

Now let's simulate a real scenario. We create a "dirty" recording: a voice buried under a loud hum.

```python
# Create a dirty recording: voice (our mono sample) + a loud hum
# First, generate a hum that matches the sample length
t_sample = np.arange(len(sample)) / rate
noise = (np.sin(2 * np.pi * 220 * t_sample) * 15000).astype(np.int16)

# Mix: voice + noise (use float to avoid overflow)
dirty = np.clip(
    sample.astype(np.float64) + noise.astype(np.float64),
    -32768, 32767
).astype(np.int16)

print(f"Sample shape: {sample.shape}")
print(f"Noise shape: {noise.shape}")
print(f"Dirty shape: {dirty.shape}")
```

**Task:** Implement `cancel_noise()` — subtract the known noise from the dirty recording.

```python
def cancel_noise(dirty, noise):
    """Remove known noise from a recording by subtraction.

    Args:
        dirty: NumPy array (int16) — the contaminated recording
        noise: NumPy array (int16) — the known noise to remove

    Returns:
        NumPy array (int16) — the cleaned signal
    """
    # TODO: Implement
    # Step 1: Trim to the shorter signal's length (use min(len(dirty), len(noise)))
    # Step 2: Convert both to float64
    # Step 3: Subtract: cleaned = dirty - noise
    # Step 4: Clip and cast back to int16
    pass
```

```python
# Test noise cancellation
cleaned = cancel_noise(dirty, noise)

# See-Then-Hear: before vs after
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
for ax, signal, title, color in zip(axes,
    [dirty, noise, cleaned],
    ['Dirty Recording (Voice + Hum)', 'Known Noise (220 Hz Hum)', 'Cleaned (Dirty - Noise)'],
    ['steelblue', 'crimson', 'green']):
    t = np.arange(len(signal)) / rate
    ax.plot(t, signal, linewidth=0.5, color=color)
    ax.set_title(title)
    ax.set_ylabel('Amplitude')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
plt.show()

print("Dirty (voice buried in hum):")
display(Audio(data=dirty, rate=rate))
print("Cleaned (hum removed):")
display(Audio(data=cleaned, rate=rate))
```

**Verification:** The cleaned audio should sound like the original sample with the hum removed.

**Question:** In real forensics, why is perfect noise cancellation rare? What would happen if the hum in the dirty recording was slightly different from your `noise` reference? (Hint: the subtraction would not be exactly zero.)

---

## Phase 3: The Grand Canyon Effect — Echo (45 min)

An echo happens when sound bounces off a surface (like a canyon wall) and reaches your ears a moment later. We can simulate this digitally by creating a delayed, quieter copy of the audio and mixing it with the original.

---

### Part A: Understanding Echo (10 min)

**The Math (Precalculus: Horizontal Translation + Vertical Scaling):**

```
echo(x) = f(x) + decay × f(x - delay)
```

- `f(x - delay)` shifts the function to the right (the sound arrives later)
- `decay` scales it vertically (the echo is quieter than the original)

**How it works with arrays:**

```
Original:  [s0  s1  s2  s3  s4  s5  s6  s7][  0   0   0 ]   ← pad end
Delayed:   [  0   0   0 ][s0  s1  s2  s3  s4  s5  s6  s7]   ← pad start
                 ↑ delay (3 samples of silence)

Mix = Original + decay × Delayed
```

Both arrays are the same total length. The delayed version is just the original with zeros added to the front (representing silence before the echo arrives). We pad the original's end with zeros to match.

---

### Part B: Implementing Echo (20 min)

```python
def add_echo(data, rate, delay_seconds=0.3, decay=0.4):
    """Add a single echo to audio data.

    Args:
        data: NumPy array, dtype int16 (mono)
        rate: int, sample rate in Hz
        delay_seconds: float, echo delay in seconds
        decay: float, echo volume relative to original (0.0 to 1.0)

    Returns:
        NumPy array, dtype int16 (longer than input by delay_samples)
    """
    delay_samples = int(delay_seconds * rate)

    # TODO: Implement
    # Step 1: Create the delayed copy — pad the FRONT with zeros
    #   delayed = np.concatenate([np.zeros(delay_samples, dtype=np.int16), data])

    # Step 2: Pad the ORIGINAL to match the delayed array's length
    #   original_padded = np.concatenate([data, np.zeros(delay_samples, dtype=np.int16)])

    # Step 3: Mix — convert to float64, combine, clip, cast back
    #   mixed = original_padded.astype(np.float64) + decay * delayed.astype(np.float64)
    #   return np.clip(mixed, -32768, 32767).astype(np.int16)

    pass
```

```python
# Test echo with different parameters
echo_short = add_echo(sample, rate, delay_seconds=0.3, decay=0.4)
echo_long = add_echo(sample, rate, delay_seconds=0.6, decay=0.5)

print(f"Original: {len(sample)} samples ({len(sample)/rate:.2f}s)")
print(f"Echo 0.3s: {len(echo_short)} samples ({len(echo_short)/rate:.2f}s)")
print(f"Echo 0.6s: {len(echo_long)} samples ({len(echo_long)/rate:.2f}s)")
```

<details>
<summary>Expected Output</summary>

```
Original: 64000 samples (4.00s)
Echo 0.3s: 68800 samples (4.30s)
Echo 0.6s: 73600 samples (4.60s)
```

The output is longer than the input because the echo extends past the end of the original sound.
</details>

```python
# See-Then-Hear: compare original with both echo versions
fig, axes = plt.subplots(3, 1, figsize=(12, 8))
for ax, signal, title in zip(axes,
    [sample, echo_short, echo_long],
    ['Original', 'Echo (0.3s delay, 0.4 decay)', 'Echo (0.6s delay, 0.5 decay)']):
    t = np.arange(len(signal)) / rate
    ax.plot(t, signal, linewidth=0.5, color='steelblue')
    ax.set_title(title)
    ax.set_ylabel('Amplitude')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
plt.show()

print("Original:")
display(Audio(data=sample, rate=rate))
print("Echo (0.3s, 0.4 decay):")
display(Audio(data=echo_short, rate=rate))
print("Echo (0.6s, 0.5 decay):")
display(Audio(data=echo_long, rate=rate))
```

**Question:** What happens if `decay >= 1.0`? Why would this be a problem in a real audio system? (Hint: each echo would be as loud or louder than the original.)

---

### Part C: Multi-Echo / Reverb (Bonus — 15 min)

Real rooms produce many reflections. We can simulate reverb by stacking multiple echoes, each one delayed further and decayed more.

**The Math:**

```
reverb(x) = f(x) + decay¹ × f(x - d) + decay² × f(x - 2d) + decay³ × f(x - 3d) + ...
```

Each successive echo is `decay` times quieter than the previous one.

```python
def add_reverb(data, rate, num_echoes=4, delay_seconds=0.15, decay=0.5):
    """Add multiple decaying echoes to simulate room reverb.

    Args:
        data: NumPy array, dtype int16 (mono)
        rate: int, sample rate
        num_echoes: int, number of echo reflections
        delay_seconds: float, delay between each reflection
        decay: float, volume decay per reflection (compounds: decay^n)

    Returns:
        NumPy array, dtype int16
    """
    delay_samples = int(delay_seconds * rate)
    total_delay = num_echoes * delay_samples
    total_length = len(data) + total_delay

    # TODO: Implement
    # Start with the original, padded to total length
    # result = np.zeros(total_length, dtype=np.float64)
    # result[:len(data)] = data.astype(np.float64)
    #
    # For each echo n (1 to num_echoes):
    #   offset = n * delay_samples
    #   volume = decay ** n
    #   result[offset:offset+len(data)] += data.astype(np.float64) * volume
    #
    # Clip and cast back to int16
    pass
```

```python
# Test reverb
reverb = add_reverb(sample, rate, num_echoes=5, delay_seconds=0.1, decay=0.5)

fig, axes = plt.subplots(2, 1, figsize=(12, 6))
axes[0].plot(np.arange(len(sample)) / rate, sample, linewidth=0.5, color='steelblue')
axes[0].set_title('Original (Dry)')
axes[1].plot(np.arange(len(reverb)) / rate, reverb, linewidth=0.5, color='darkorange')
axes[1].set_title('With Reverb (5 echoes, 0.1s spacing, 0.5 decay)')
for ax in axes:
    ax.set_ylabel('Amplitude')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
plt.show()

print("Dry:")
display(Audio(data=sample, rate=rate))
print("Reverb:")
display(Audio(data=reverb, rate=rate))
```

---

## Phase 4: Time Travel & Pitch (30 min)

Array slicing gives us the power to manipulate time itself — playing audio backward and changing its speed.

---

### Part A: Reversal — Playing Backwards (10 min)

**Goal:** Reverse the entire audio signal using array slicing.

**The Math (Precalculus: Reflection over y-axis):**

```
reversed = f(-x)    →    data[::-1]
```

**Implementation:**

```python
reversed_audio = sample[::-1].copy()
# .copy() is important! [::-1] creates a "view" with negative strides,
# which can cause issues with wavfile.write(). .copy() creates a contiguous array.
```

```python
# See-Then-Hear: forward vs backward
fig, axes = plt.subplots(2, 1, figsize=(12, 5), sharex=True)
t = np.arange(len(sample)) / rate

axes[0].plot(t, sample, linewidth=0.5, color='steelblue')
axes[0].set_title('Original (Forward)')

axes[1].plot(t, reversed_audio, linewidth=0.5, color='purple')
axes[1].set_title('Reversed (Backward)')

for ax in axes:
    ax.set_ylabel('Amplitude')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
plt.show()

print("Forward:")
display(Audio(data=sample, rate=rate))
print("Reversed:")
display(Audio(data=reversed_audio, rate=rate))
```

**Discovery:** Reversed audio sounds alien and unrecognizable — but the waveform is simply the mirror image read from right to left.

---

### Part B: Speed & Pitch — Skipping Samples (10 min)

**Goal:** Change playback speed (and pitch) by resampling the array.

**The Math (Precalculus: Horizontal Compression/Stretch):**

```
faster = f(2x)    →    data[::2]     (skip every other sample → half duration, double pitch)
slower = f(x/2)   →    np.repeat()   (duplicate each sample → double duration, half pitch)
```

**Simple approach — integer factors:**

```python
# Double speed (skip every other sample)
fast_simple = sample[::2]
print(f"Original: {len(sample)} samples ({len(sample)/rate:.2f}s)")
print(f"Fast (::2): {len(fast_simple)} samples ({len(fast_simple)/rate:.2f}s)")
```

**Better approach — arbitrary speed factors using interpolation:**

```python
def change_speed(data, factor):
    """Change audio speed/pitch by resampling.

    Args:
        data: NumPy array, dtype int16
        factor: float (2.0 = double speed/higher pitch, 0.5 = half speed/lower pitch)

    Returns:
        NumPy array, dtype int16
    """
    # TODO: Implement
    # new_length = int(len(data) / factor)
    # old_indices = np.linspace(0, len(data) - 1, new_length)
    # resampled = np.interp(old_indices, np.arange(len(data)), data.astype(np.float64))
    # return resampled.astype(np.int16)
    pass
```

```python
# Test speed changes
fast = change_speed(sample, 2.0)
slow = change_speed(sample, 0.5)

print(f"Original: {len(sample)} samples ({len(sample)/rate:.2f}s)")
print(f"Fast (2.0×): {len(fast)} samples ({len(fast)/rate:.2f}s)")
print(f"Slow (0.5×): {len(slow)} samples ({len(slow)/rate:.2f}s)")
```

<details>
<summary>Expected Output</summary>

```
Original: 64000 samples (4.00s)
Fast (2.0×): 32000 samples (2.00s)
Slow (0.5×): 128000 samples (8.00s)
```

Doubling the speed halves the number of samples (and duration). Halving the speed doubles them.
</details>

```python
# See-Then-Hear: compare all three
fig, axes = plt.subplots(3, 1, figsize=(12, 8))
for ax, signal, title in zip(axes,
    [sample, fast, slow],
    ['Original (1.0×)', 'Fast (2.0× speed, higher pitch)', 'Slow (0.5× speed, lower pitch)']):
    t = np.arange(len(signal)) / rate
    ax.plot(t, signal, linewidth=0.5, color='steelblue')
    ax.set_title(title)
    ax.set_ylabel('Amplitude')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
plt.show()

print("Original:")
display(Audio(data=sample, rate=rate))
print("2× Speed (chipmunk):")
display(Audio(data=fast, rate=rate))
print("0.5× Speed (slow-mo):")
display(Audio(data=slow, rate=rate))
```

**Question:** Why does speeding up audio also raise the pitch? (Hint: the same number of oscillations are squeezed into less time, which means more vibrations per second = higher frequency.)

---

### Part C: Saving Processed Audio (10 min)

**Goal:** Save any transformation back to a WAV file using `wavfile.write()`.

```python
def save_audio(filename, data, rate):
    """Save audio data to a WAV file.

    Args:
        filename: str, output file path
        data: NumPy array, dtype int16
        rate: int, sample rate in Hz
    """
    wavfile.write(filename, rate, data.astype(np.int16))
```

**Task:** Save the reversed audio and the echo version:

```python
save_audio('data/reversed_output.wav', reversed_audio, rate)
save_audio('data/echo_output.wav', echo_short, rate)

print("Files saved:")
print("  data/reversed_output.wav")
print("  data/echo_output.wav")
```

**Verification:** Load the saved files back and confirm they match:

```python
# Round-trip test
rate_check, loaded = wavfile.read('data/reversed_output.wav')
print(f"Saved and loaded match: {np.array_equal(reversed_audio, loaded)}")
```

<details>
<summary>Expected Output</summary>

```
Saved and loaded match: True
```
</details>

---

## Phase 5: Critical Incident — "The Ghost in the Machine" (30 min)

**The Escalation:** A recording (`mystery.wav`) recovered from a suspect's laptop produces only an unpleasant hum when played. Intelligence suggests the original voice message was **reversed** and **buried under a loud synthetic hum** to prevent casual listening. A clean sample of the hum (`pure_hum.wav`) was found in the same directory.

Your mission: **recover the hidden message using the toolkit you just built.**

---

### Step 1: Initial Assessment (5 min)

Load and inspect the mystery recording. What do you see? What do you hear?

```python
rate_m, mystery = wavfile.read('data/mystery.wav')

print(f"Sample Rate: {rate_m} Hz")
print(f"Shape: {mystery.shape}")
print(f"Dtype: {mystery.dtype}")
print(f"Duration: {len(mystery) / rate_m:.2f} seconds")
print(f"Min: {mystery.min()}, Max: {mystery.max()}")
```

```python
# Visualize the raw mystery recording
fig, ax = plt.subplots(figsize=(12, 4))
t = np.arange(len(mystery)) / rate_m
ax.plot(t, mystery, linewidth=0.5, color='steelblue')
ax.set_title('Mystery Recording — Raw')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude')
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

print("Mystery (raw):")
display(Audio(data=mystery, rate=rate_m))
```

**Observation:** Can you hear anything intelligible? The waveform looks like a regular sine wave (the hum) with some disturbance. The hum dominates.

---

### Step 2: Cancel the Hum (10 min)

Load the pure hum file and subtract it from the mystery recording.

```python
rate_h, pure_hum = wavfile.read('data/pure_hum.wav')

print(f"Pure hum — Rate: {rate_h} Hz, Shape: {pure_hum.shape}, Duration: {len(pure_hum)/rate_h:.2f}s")
print(f"Mystery  — Rate: {rate_m} Hz, Shape: {mystery.shape}, Duration: {len(mystery)/rate_m:.2f}s")
```

```python
# TODO: Cancel the hum from the mystery recording
# Hint: Use your cancel_noise() function from Phase 2
# The pure_hum is longer than mystery — cancel_noise() should handle trimming

cleaned = cancel_noise(mystery, pure_hum)
```

```python
# Visualize before/after cancellation
fig, axes = plt.subplots(2, 1, figsize=(12, 5), sharex=True)

axes[0].plot(np.arange(len(mystery)) / rate_m, mystery, linewidth=0.5, color='steelblue')
axes[0].set_title('Before: Mystery (Voice + Hum)')

axes[1].plot(np.arange(len(cleaned)) / rate_m, cleaned, linewidth=0.5, color='green')
axes[1].set_title('After: Hum Cancelled')

for ax in axes:
    ax.set_ylabel('Amplitude')
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
axes[-1].set_xlabel('Time (seconds)')
plt.tight_layout()
plt.show()

print("After hum cancellation:")
display(Audio(data=cleaned, rate=rate_m))
```

**Observation:** The hum should be gone, but the remaining audio still sounds strange — it is played backward!

---

### Step 3: Reverse the Cleaned Signal (5 min)

The hidden message was recorded backward. Flip it.

```python
# TODO: Reverse the cleaned audio
# Hint: Use [::-1].copy()

recovered = cleaned[::-1].copy()
```

```python
# Listen to the reversed result
fig, ax = plt.subplots(figsize=(12, 4))
t = np.arange(len(recovered)) / rate_m
ax.plot(t, recovered, linewidth=0.5, color='purple')
ax.set_title('Reversed — Can You Hear the Message?')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude')
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

print("Reversed:")
display(Audio(data=recovered, rate=rate_m))
```

**Observation:** You should be able to hear speech now, but it may be very quiet.

---

### Step 4: Boost the Volume (5 min)

Scale the recovered signal so it is clearly audible.

```python
# TODO: Boost the volume of the recovered message
# Hint: Use your adjust_volume() function
# Choose a factor that makes the message clearly audible without distortion

peak = max(abs(recovered.min()), abs(recovered.max()))
boost_factor = 30000 / peak  # Scale peak to ~30000 (leaving headroom)
print(f"Peak amplitude: {peak}")
print(f"Boost factor: {boost_factor:.2f}")

final = adjust_volume(recovered, boost_factor)
```

```python
# Final result — the recovered message
fig, ax = plt.subplots(figsize=(12, 4))
t = np.arange(len(final)) / rate_m
ax.plot(t, final, linewidth=0.5, color='green')
ax.set_title('RECOVERED MESSAGE')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude')
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

print("RECOVERED MESSAGE:")
display(Audio(data=final, rate=rate_m))
```

**Task:** Listen carefully and transcribe the recovered message. Write it down in [`submission.md`](submission.md).

---

### Step 5: The Full Recovery Pipeline (5 min)

Now combine everything into a single function — this is your complete forensic audio recovery tool.

```python
def recover_message(mystery_path, hum_path):
    """Complete forensic audio recovery pipeline.

    Steps:
        1. Load both audio files
        2. Cancel the hum (subtract noise)
        3. Reverse the result
        4. Boost volume for audibility

    Args:
        mystery_path: str, path to the mystery recording
        hum_path: str, path to the known hum file

    Returns:
        tuple: (recovered_data as int16, sample_rate)
    """
    # TODO: Implement the complete pipeline
    # Step 1: Load both files using wavfile.read()

    # Step 2: Cancel the hum using cancel_noise()

    # Step 3: Reverse using [::-1].copy()

    # Step 4: Boost volume using adjust_volume()
    #   (calculate boost factor from peak amplitude)

    # Step 5: Return (recovered_data, sample_rate)
    pass
```

```python
# Test the complete pipeline
recovered_final, rate_final = recover_message('data/mystery.wav', 'data/pure_hum.wav')

# Save the recovered message
save_audio('data/recovered_message.wav', recovered_final, rate_final)

print("Recovered message saved to data/recovered_message.wav")
print("\nFinal playback:")
display(Audio(data=recovered_final, rate=rate_final))
```

---

## Wrap-Up

Congratulations, analyst. You have:

1. **Loaded** WAV audio files as NumPy arrays and understood mono vs. stereo structure.
2. **Visualized** waveforms with proper time axes and played audio directly in the notebook.
3. **Built** five audio effects from scratch using only array math — volume control, phase inversion, noise cancellation, echo, and reversal.
4. **Discovered** the int16 overflow trap (the audio equivalent of Lab 04's uint8 overflow).
5. **Recovered** a hidden spoken message using a multi-step forensic pipeline.

Every effect you implemented maps to a Precalculus function transformation:

| Effect | Transformation | Code |
|--------|----------------|------|
| Volume | $A \cdot f(x)$ | `data * factor` |
| Inversion | $-f(x)$ | `-data` |
| Cancellation | $f(x) + (-f(x)) = 0$ | `signal - noise` |
| Echo | $f(x) + d \cdot f(x-h)$ | `original + decay * delayed` |
| Reversal | $f(-x)$ | `data[::-1]` |
| Speed | $f(cx)$ | `data[::c]` or `np.interp` |

### Before You Leave

- [ ] Complete all sections of [`submission.md`](submission.md)
- [ ] Ensure all notebook cells run without errors from top to bottom
- [ ] Verify the recovered message is transcribed correctly
- [ ] Include the AI Usage Appendix if applicable

### Looking Ahead

The array manipulation skills you practiced here — slicing, broadcasting, vectorized math, overflow protection — are the same ones used in data science for processing streaming data, financial time series, and sensor arrays. Sound is just the beginning.
