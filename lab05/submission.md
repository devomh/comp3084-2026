# Lab 05 Submission: Digital Waves

**Student Name:** [Your Name]
**Date:** [Date]

## Section A: Audio Loading & Inspection

### Audio File Properties

| Property | stereo_sample.wav | pure_hum.wav | mystery.wav |
|----------|-------------------|--------------|-------------|
| Sample Rate (Hz) | | | |
| Shape | | | |
| Dtype | | | |
| Duration (seconds) | | | |
| Min / Max | | | |
| Mono or Stereo? | | | |

## Section B: Audio Effect Implementations

### Stereo-to-Mono
- [ ] Channel averaging implemented
- [ ] float64 conversion to avoid overflow
- [ ] Output dtype: int16
- [ ] Verified by playback (sounds same as stereo)

### Volume Control
- [ ] Scalar multiplication implemented
- [ ] float64 conversion to avoid int16 overflow
- [ ] np.clip() applied to [-32768, 32767]
- [ ] Tested with factor=2.0 and factor=0.3

### Phase Inversion
- [ ] Negation implemented (`-data`)
- [ ] Visual verification: waveform flipped across x-axis
- [ ] Auditory verification: sounds identical to original

### Noise Cancellation
- [ ] Perfect cancellation demo: signal + anti-signal = all zeros
- [ ] cancel_noise() function implemented
- [ ] Forensic hum removal tested and verified by playback

### Echo Effect
- [ ] add_echo() function implemented
- [ ] Delay via zero-padding (np.concatenate)
- [ ] Decay scaling applied
- [ ] Tested with delay=0.3s and delay=0.6s

### Reversal
- [ ] data[::-1].copy() used
- [ ] Verified by playback (sounds reversed)

### Speed Change
- [ ] change_speed() function implemented
- [ ] Tested with factor=2.0 (chipmunk) and factor=0.5 (slow-mo)

## Section C: Critical Incident — Message Recovery

### Recovered Message Transcription
[Write the spoken words you heard in the recovered message here]

### Recovery Process
1. [Describe step 1 — what did you do and why?]
2. [Describe step 2]
3. [Describe step 3]
4. [Describe step 4]

### Pipeline Verification
- [ ] Hum successfully cancelled
- [ ] Reversed audio produces intelligible speech
- [ ] Volume boosted for audibility
- [ ] recover_message() function produces correct output
- [ ] Recovered audio saved to data/recovered_message.wav

## Section D: Reflections

1. Why does phase inversion (`-data`) sound identical to the original, even
   though the waveform looks completely different?

2. What happens if you perform arithmetic on int16 arrays without converting
   to float64 first? Give a specific example with numbers.

3. In real-world forensics, why is perfect noise cancellation rarely possible?
   What conditions must be met for subtraction-based cancellation to work?

4. Why does doubling the speed of audio also raise its pitch? What is the
   relationship between sample rate, frequency, and pitch?

## Section E: Bonus (if attempted)

### Multi-Echo Reverb
- [ ] add_reverb() function implemented
- [ ] Compounding decay (decay^n) across N echoes
- [ ] Verified by playback

### Speed Change (Interpolation)
- [ ] np.interp used for smooth resampling
- [ ] Tested with non-integer factor (e.g., 1.5)

### Fade In/Out
- [ ] Linear amplitude ramp at start/end of audio
- [ ] Verified: no clicking at boundaries

## Section F: AI Usage (if applicable)

### Tool Used
[Name of AI tool]

### Methodology
[How did you use it? What was your approach?]

### The Prompt
[Paste the prompt you used]

### The Output
[Paste the AI's response]

### Human Value-Add
[What did you change, verify, or learn from the AI's output?]
