# Lab 05: Digital Waves

**Concepts**: [![Open Concepts In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab05/concepts.ipynb)

**Lab05**: [![Open Lab Notebook In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/devomh/comp3084-2026/blob/main/lab05/lab05.ipynb)

## Case Brief

### The Situation

The Audio Forensics Division has received a suspicious recording (`mystery.wav`)
recovered from a seized laptop. Initial playback reveals only an unpleasant,
constant hum — no intelligible content. However, intelligence analysts suspect
the original message was **reversed** and **buried under a synthetic hum** to
prevent casual listening. Standard audio players cannot recover it.

### Your Mission

You are an **Audio Forensics Analyst** tasked with building a custom audio
analysis toolkit from scratch and using it to recover the hidden message.
You will:

1. Load WAV audio files as NumPy arrays and understand their structure.
2. Visualize waveforms and listen to audio directly inside the notebook.
3. Build audio effects (volume, noise cancellation, echo, reversal, speed
   change) using only raw array mathematics.
4. Recover a hidden spoken message from `mystery.wav` using the techniques
   you built.

### The Stakes

The recovered audio may contain critical operational intelligence. Each
transformation you implement is a forensic tool — volume scaling reveals
quiet signals, noise cancellation strips interference, and reversal undoes
deliberate obfuscation. Every function must be correct, and every result
must be verified both visually (waveform plots) and audibly (playback).

---

## Chain of Custody

### Technical Requirements

- Completion of Lab 04 (NumPy arrays, vectorized operations)
- Python 3.8 or higher
- Python libraries: `numpy`, `scipy`, `matplotlib`, `IPython`

```bash
pip install numpy scipy matplotlib
```

**Library Constraints (strictly enforced):**

- **`scipy.io.wavfile`** — only `read()` and `write()`
- **`numpy`** — all array operations allowed
- **`matplotlib`** — `plot()`, `subplots()`, `show()`, axis labels and titles
- **`IPython.display`** — `Audio()` and `display()` for playback
- **No `librosa`, `pydub`, `soundfile`, `scipy.signal`**, or any DSP library

### Evidence Files (Provided)

Located in the [`data/`](data/) directory:

1. **`stereo_sample.wav`** — High-quality stereo clip for loading, visualization,
   echo, and stereo-to-mono exercises
2. **`pure_hum.wav`** — Clean 220 Hz sine wave hum (matches the noise in the
   mystery recording)
3. **`mystery.wav`** — Suspected carrier of hidden spoken message (the Critical
   Incident)

```bash
# Verify the evidence files are present
ls data/
# Expected: stereo_sample.wav  pure_hum.wav  mystery.wav
```

---

## Investigation Phases

Open [`lab05.md`](lab05.md) (or [`lab05.ipynb`](lab05.ipynb) in Jupyter/Colab) for
the guided exercises. Consult [`concepts.md`](concepts.md) for technical background.

### Phase 1: The Sound as a List (30 min)

**Objective:** Understand how digital audio maps to a NumPy array.

- Load WAV files using `scipy.io.wavfile.read()`
- Inspect shape, dtype, sample rate, and duration
- Distinguish mono (1D) from stereo (2D) arrays
- Visualize waveforms with Matplotlib (full view and zoomed window)
- Listen using `IPython.display.Audio` playback widgets
- Convert stereo to mono by averaging channels

**Key insight:** A sound is a 1D array of amplitudes (heights) sampled at a
fixed rate. A stereo sound has two columns — left and right.

---

### Phase 2: The "Anti-Sound" & Volume (45 min)

**Objective:** Apply scalar multiplication and additive inverse to audio signals.

#### Part A: Volume Control — Vertical Scaling (15 min)

Implement `adjust_volume()` using scalar multiplication:

```
louder  = factor × signal,    where factor > 1
quieter = factor × signal,    where 0 < factor < 1
```

**int16 overflow warning:** `np.int16(20000) * np.int16(2) = -25536` (wraps!).
Always convert to `float64` before arithmetic, clip to `[-32768, 32767]`, then
cast back.

#### Part B: Phase Inversion (10 min)

Multiply by `-1` to flip the waveform across the x-axis. Discovery: it
*sounds identical* to the original — the human ear perceives amplitude
patterns, not polarity.

#### Part C: Noise Cancellation — Destructive Interference (20 min)

Demonstrate that `signal + (-signal) = 0` (perfect silence). Then apply this
principle forensically: subtract a known hum from a contaminated recording
to reveal the voice underneath.

---

### Phase 3: The Grand Canyon Effect — Echo (45 min)

**Objective:** Build an echo effect using array concatenation and mixing.

#### Part A: Understanding Echo (10 min)

An echo is `f(x) + decay × f(x - delay)` — a horizontal shift (delay) combined
with vertical scaling (decay).

#### Part B: Single Echo (20 min)

Implement `add_echo()` by padding with zeros and mixing:

```python
delayed = np.concatenate([np.zeros(delay_samples), data])
original_padded = np.concatenate([data, np.zeros(delay_samples)])
result = original_padded + decay * delayed
```

#### Part C: Multi-Echo Reverb (15 min)

Stack multiple decaying echoes to simulate room reverb. Each reflection is
quieter: `decay^n`.

---

### Phase 4: Time Travel & Pitch (30 min)

**Objective:** Reverse and resample audio using array slicing.

- **Reversal:** `data[::-1]` plays audio backward (reflection over y-axis)
- **Speed/Pitch:** `data[::2]` doubles speed and raises pitch; resampling with
  `np.interp` allows arbitrary speed factors
- **Saving:** Use `wavfile.write()` to export processed audio

---

### Phase 5: Critical Incident — "The Ghost in the Machine" (30 min)

**Objective:** Recover a hidden spoken message from `data/mystery.wav`.

**Intel:** The original message was (1) reversed, (2) buried under a 220 Hz
synthetic hum, and (3) possibly attenuated.

**Recovery procedure:**

1. **Load and assess** — visualize and listen to the raw mystery recording
2. **Cancel the hum** — subtract `pure_hum.wav` from the mystery signal
3. **Reverse** — flip the cleaned audio to restore original word order
4. **Boost volume** — scale up the recovered signal for clarity
5. **Transcribe** — write down the spoken message

Implement `recover_message()` as a complete pipeline combining all techniques
from Phases 2–4.

---

## Wrap-Up

After completing all phases, verify the full recovery pipeline produces
intelligible speech, then run each cell from top to bottom to confirm
everything works.

**Before you leave:**

- Complete all sections of [`submission.md`](submission.md), including the
  transcribed message and reflection questions.
- Ensure all notebook cells run without errors from top to bottom.
- Include your AI Usage Appendix if applicable.

---

## Submission Requirements

### 1. Notebook

- [`lab05.ipynb`](lab05.ipynb) — All cells implemented and run without errors,
  top to bottom

### 2. Documentation

Complete [`submission.md`](submission.md) with:

- Audio file properties table (shape, dtype, sample rate, duration)
- Transcribed hidden message from the Critical Incident
- Answers to all reflection questions

---

## Evaluation Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Loading & Inspection** | 10 | Shape, dtype, rate, duration reported; mono vs. stereo identified |
| **Waveform Visualization** | 10 | Time axis in seconds, labeled axes, zero line, windowed view |
| **Stereo-to-Mono** | 5 | Correct channel averaging, verified by playback |
| **Volume Control** | 10 | Correct scaling with overflow protection; before/after comparison |
| **Phase Inversion** | 5 | Correct negation; visual verification of flip |
| **Noise Cancellation** | 15 | Perfect cancellation demo; forensic hum removal with playback |
| **Echo Effect** | 15 | Correct delay + decay mixing; verified visually and audibly |
| **Reversal & Speed** | 10 | Correct slicing; playback verification |
| **Critical Incident** | 20 | Full pipeline works; message transcribed correctly |
| **Total** | **100** | |

**Bonus:**

| Component | Points | Criteria |
|-----------|--------|----------|
| Multi-Echo Reverb | +5 | Compounding decay across N echoes |
| Speed Change (interpolation) | +5 | Smooth resampling using `np.interp` |
| Fade In/Out Effect | +5 | Linear amplitude ramp at start/end |

---

## Tips for Success

1. **Read the Field Manual first:** [`concepts.md`](concepts.md) covers sound
   representation, sample rates, int16 arithmetic, and function transformations
   with worked examples and annotated plots.

2. **Watch out for int16 overflow:** This is the most common bug in this lab.
   Before any arithmetic on audio data, cast to `float64`. After clipping to
   `[-32768, 32767]`, cast back to `int16`.

3. **Follow the See-Then-Hear pattern:** Every transformation should be
   verified in two ways:
   - **See:** Plot the waveform to confirm the shape changed as expected
   - **Hear:** Play the audio to confirm it sounds correct

4. **Test incrementally:** After implementing each function, immediately test
   and verify before moving on:
   ```python
   result = adjust_volume(data, 2.0)
   print(result.shape, result.dtype, result.min(), result.max())
   ```

5. **Keep audio mono for simplicity:** Convert stereo to mono early. All
   processing functions expect 1D arrays.

6. **Use `.copy()` after reversal:** `data[::-1]` creates a *view* with
   negative strides, which can cause issues with `wavfile.write()`. Use
   `data[::-1].copy()` to get a contiguous array.

---

## Academic Integrity Reminder

Audio forensics is a real discipline used in law enforcement and intelligence.
You must:

- Understand every transformation you implement and explain the math behind it
- Be able to explain why `signal + (-signal) = 0` and how this enables noise
  cancellation
- Explain how echo maps to horizontal translation in function notation
- Document any AI assistance in the AI Usage Appendix

**Remember:** In a real forensic investigation, presenting results you cannot
explain or verify is inadmissible. Build it, understand it, own it.

---

## Resources

- **Field Manual:** [`concepts.md`](concepts.md) — Sound representation, sample
  rates, int16 overflow, function transformations, and annotated plots
- **Lab Notebook:** [`lab05.md`](lab05.md) — Guided exercises with boilerplate
  code and expected outputs
- **Python `numpy` documentation:** [numpy.org/doc](https://numpy.org/doc/)
- **Scipy WAV I/O:** [scipy.io.wavfile](https://docs.scipy.org/doc/scipy/reference/io.html#module-scipy.io.wavfile)
- **Matplotlib `plot`:** [matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html)

---

## Questions?

If you encounter issues:

1. Re-read the relevant section in [`concepts.md`](concepts.md)
2. Check for int16 overflow — convert to `float64` before arithmetic
3. Print intermediate values, shapes, and dtypes to isolate problems
4. Verify round-trips: transform, check shape/dtype, plot, listen

**Remember:** The goal is to think like a forensic analyst — every sample
tells a story, and the tools you build determine what stories you can hear.
