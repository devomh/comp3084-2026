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

Run this cell first. Every code cell in this notebook depends on these imports and
helper functions (defined in [`concepts.md`](concepts.md)).

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from IPython.display import Audio, display

RATE = 16000  # Sample rate used throughout this lab
```

### Helper Functions — Our Audio Toolkit

These three helpers keep later code compact and enforce the **See-Then-Hear**
pattern from `concepts.md`. Run this cell before any exercise.

```python
def generate_note(freq, duration=2.0, rate=RATE, amplitude=10000):
    """Generate a pure sine wave at the given frequency.

    Args:
        freq: float, frequency in Hz (e.g., 440.0 for A4)
        duration: float, length in seconds (default 2.0)
        rate: int, sample rate in Hz (default 16000)
        amplitude: int, peak amplitude (default 10000)

    Returns:
        NumPy array of shape (int(rate * duration),), dtype int16
    """
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    samples = (np.sin(2 * np.pi * freq * t) * amplitude).astype(np.int16)
    return samples


def compare_sounds(s1, s2, label1='Signal 1', label2='Signal 2',
                   rate=RATE, layout='side', zoom=1.0,
                   color1='steelblue', color2='crimson',
                   normalize=False):
    """Plot and play two sound arrays for comparison.

    Args:
        s1, s2: NumPy arrays (int16 or float) — the two signals to compare.
        label1, label2: str — display names for each signal.
        rate: int — sample rate in Hz.
        layout: 'side' for stacked subplots, 'overlap' for same axes.
        zoom: float in (0, 1] — fraction of the signal to display.
              1.0 = full signal, 0.1 = first 10% (zoomed in).
        color1, color2: matplotlib color names for each signal.
        normalize: Whether Audio playback is normalized or not. Default False
    """
    n1 = max(1, int(len(s1) * zoom))
    n2 = max(1, int(len(s2) * zoom))
    t1 = np.arange(n1) / rate
    t2 = np.arange(n2) / rate

    zoom_label = f' (zoom={zoom})' if zoom < 1.0 else ''

    if layout == 'overlap':
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(t1, s1[:n1], color=color1, linewidth=1.5, alpha=0.8, label=label1)
        ax.plot(t2, s2[:n2], color=color2, linewidth=1.5, alpha=0.8, label=label2)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Amplitude')
        ax.set_title(f'{label1} vs {label2}{zoom_label}')
        ax.legend()
        plt.tight_layout()
        plt.show()
    else:
        fig, axes = plt.subplots(2, 1, figsize=(12, 5))
        axes[0].plot(t1, s1[:n1], color=color1, linewidth=1.0)
        axes[0].set_title(f'{label1}{zoom_label}')
        axes[0].set_ylabel('Amplitude')
        axes[0].axhline(y=0, color='gray', linestyle='--', linewidth=0.5)

        axes[1].plot(t2, s2[:n2], color=color2, linewidth=1.0)
        axes[1].set_title(f'{label2}{zoom_label}')
        axes[1].set_ylabel('Amplitude')
        axes[1].axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        axes[1].set_xlabel('Time (seconds)')

        plt.tight_layout()
        plt.show()

    print(f"{label1}:")
    if normalize:
        display(Audio(data=s1, rate=rate, normalize=True))
    else:
        display(Audio(data=s1.astype(np.float32) / 32768.0, rate=rate, normalize=False))
    print(f"{label2}:")
    if normalize:
        display(Audio(data=s2, rate=rate, normalize=True))
    else:
        display(Audio(data=s2.astype(np.float32) / 32768.0, rate=rate, normalize=False))


def play(signal, label='', rate=RATE):
    """Play a single signal with an optional label."""
    if label:
        print(f"{label}:")
    display(Audio(data=signal, rate=rate))
```

---

## Phase 1: The Sound as a List (20 min)

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

### Exercise 1.2: Visualizing and Listening

Numbers alone do not tell the whole story. We need to *see* and *hear* the sound. Use `compare_sounds` to compare the left and right channels — this follows the **See-Then-Hear** pattern we will use for every transformation.

```python
# Compare left vs right channels
left_channel = data[:, 0]
right_channel = data[:, 1]

compare_sounds(left_channel, right_channel,
               'Left Channel', 'Right Channel', rate=rate, zoom=0.05)
```

**Convention (IMPORTANT):** From this point on, every transformation follows the **See-Then-Hear** pattern:

1. **Transform** the audio
2. **See** — plot the waveform
3. **Hear** — play the audio

The `compare_sounds` helper combines steps 2 and 3 into a single call. Use `play` when you only need to hear one signal.

**Question:** In the zoomed view, what does a single "wave" look like? Why do the sample points form a smooth curve even though they are discrete?

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
# See-Then-Hear: compare left channel vs mono result
compare_sounds(data[:, 0], mono,
               'Left Channel', 'Mono (Average of L+R)',
               rate=rate, color2='green')
```

From this point forward, we will use the mono version of our test audio. Let's assign it:

```python
# Use mono audio for all subsequent exercises
sample = to_mono(data)
```

---

## Phase 2: The "Anti-Sound" & Volume (35 min)

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
# See-Then-Hear: loud vs original
compare_sounds(sample, loud, 'Original', 'Volume × 2.0 (clipped)',
               rate=rate, zoom=0.05, color2='darkorange')
```

```python
# See-Then-Hear: quiet vs original — overlapped to compare wave heights
compare_sounds(sample, quiet, 'Original', 'Volume × 0.3',
               rate=rate, layout='overlap', zoom=0.05, color2='darkorange')
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
# See-Then-Hear: overlapped view clearly shows the mirror image
compare_sounds(sample, inverted, 'Original', 'Phase Inverted (× -1)',
               rate=rate, layout='overlap', zoom=0.02)
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

play(hum_demo, 'Hum')
play(anti_hum, 'Anti-Hum')
play(result.astype(np.int16), 'Sum (should be silent)')
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

# See-Then-Hear: dirty vs cleaned
compare_sounds(dirty, cleaned,
               'Dirty (Voice + Hum)', 'Cleaned (Dirty - Noise)',
               rate=rate, color2='green')
```

**Verification:** The cleaned audio should sound like the original sample with the hum removed.

**Question:** In real forensics, why is perfect noise cancellation rare? What would happen if the hum in the dirty recording was slightly different from your `noise` reference? (Hint: the subtraction would not be exactly zero.)

---

## Phase 3: The Grand Canyon Effect — Echo (30 min)

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
# See-Then-Hear: original vs short echo
compare_sounds(sample, echo_short,
               'Original (Dry)', 'Echo (0.3s delay, 0.4 decay)',
               rate=rate, color2='darkorange')
```

```python
# See-Then-Hear: original vs long echo
compare_sounds(sample, echo_long,
               'Original (Dry)', 'Echo (0.6s delay, 0.5 decay)',
               rate=rate, color2='darkorange')
```

**Question:** What happens if `decay >= 1.0`? Why would this be a problem in a real audio system? (Hint: each echo would be as loud or louder than the original.)

---

## Phase 4: Time Travel & Pitch (20 min)

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
compare_sounds(sample, reversed_audio,
               'Original (Forward)', 'Reversed (Backward)',
               rate=rate, color2='purple')
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
# See-Then-Hear: original vs fast
compare_sounds(sample, fast, 'Original (1.0×)', 'Fast (2.0× — chipmunk)',
               rate=rate, color2='darkorange')
```

```python
# See-Then-Hear: original vs slow
compare_sounds(sample, slow, 'Original (1.0×)', 'Slow (0.5× — slow-mo)',
               rate=rate, color2='darkorange')
```

**Question:** Why does speeding up audio also raise the pitch? (Hint: the same number of oscillations are squeezed into less time, which means more vibrations per second = higher frequency.)

---

## Phase 5: Critical Incident — "The Ghost in the Machine" (25 min)

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
# Listen to the raw mystery recording
play(mystery, 'Mystery (raw)')
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
# See-Then-Hear: before vs after cancellation
compare_sounds(mystery, cleaned,
               'Before (Voice + Hum)', 'After (Hum Cancelled)',
               rate=rate_m, color2='green')
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
# Listen — can you hear the message now?
play(recovered, 'Reversed')
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
# See-Then-Hear: the full journey — mystery vs recovered
compare_sounds(mystery, final,
               'Mystery (Raw)', 'RECOVERED MESSAGE',
               rate=rate_m, color2='green')
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
wavfile.write('data/recovered_message.wav', rate_final, recovered_final.astype(np.int16))

print("Recovered message saved to data/recovered_message.wav")
play(recovered_final, 'Final playback')
```

---

## Wrap-Up

Congratulations, analyst. You have:

1. **Loaded** WAV audio files as NumPy arrays and understood mono vs. stereo structure.
2. **Used** the `compare_sounds` / `play` toolkit to verify every transformation visually and audibly.
3. **Built** five audio effects from scratch using only array math — volume control, phase inversion, noise cancellation, echo, and speed/pitch change.
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
