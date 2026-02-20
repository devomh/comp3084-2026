# Lab 04 Submission: Matrix Vision

**Student Name:** [Your Name]
**Date:** [Date]

## Section A: Image Loading & Inspection

### Image Properties
| Property | surveillance_a.png | surveillance_b.png |
|----------|-------------------|-------------------|
| Shape    |                   |                   |
| Dtype    |                   |                   |
| Min/Max  |                   |                   |
| Size (bytes) |              |                   |

## Section B: Filter Implementations

### Grayscale
- [ ] Luminosity formula implemented
- [ ] Weights: R=0.2989, G=0.5870, B=0.1140
- [ ] Output dtype: uint8

### Inversion
- [ ] Single-operation complement
- [ ] Works on both color and grayscale

### Brightness/Contrast
- [ ] Float conversion to avoid overflow
- [ ] np.clip() applied
- [ ] Tested with alpha=1.5, beta=30

### Thresholding
- [ ] Boolean masking approach
- [ ] Tested with threshold=128

### Box Blur
- [ ] 3x3 kernel implemented
- [ ] Border handling with np.pad()
- [ ] Tested on color and grayscale

## Section C: Steganography

### Decoded Message
[Paste the hidden message here]

### Decoding Process
1. [Describe step 1]
2. [Describe step 2]
3. [Describe step 3]

### Capacity Analysis
- Image dimensions: ___ x ___
- Total Red channel pixels: ___
- Maximum hidden data: ___ bytes

## Section D: Reflections

1. Why do the luminosity weights differ across R, G, B?
2. What happens if you forget to clip after brightness adjustment?
3. How could you detect if an image contains hidden steganographic data?
4. What is the trade-off between kernel size and blur strength?

## Section E: AI Usage (if applicable)
[Standard AI appendix format]
