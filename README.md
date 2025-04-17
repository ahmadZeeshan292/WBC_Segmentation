# 🧬 Hematological Image Segmentation using Connected Component Analysis (CCA)

![Python](https://img.shields.io/badge/Language-Python-blue)
![Segmentation](https://img.shields.io/badge/Topic-Image%20Segmentation-orange)
![Algorithm](https://img.shields.io/badge/Technique-Connected%20Component%20Analysis-green)
![Metric](https://img.shields.io/badge/Metric-Dice%20Coefficient-critical)

---

## 🧪 Project Overview

This project implements a segmentation pipeline to isolate **white blood cell (WBC)** components—specifically **nucleus** and **cytoplasm**—from hematological images using **Connected Component Labeling (CCA)**. The approach includes:

- Nucleus and cytoplasm differentiation  
- Adaptive V-set thresholding  
- 8-connectivity labeling  
- Hole-filling and component filtering  
- Accuracy evaluation using the Dice Coefficient  

---

## 🔍 Key Features

### ✅ Adaptive V-Set Calculation

- Performs **15×15 local mean intensity analysis** to capture regional differences
- Dynamically calculates threshold ranges:
  - **Nucleus V-set**: min(mean) → min(mean) + 55  
  - **Cytoplasm V-set**: min(mean) + 60 → 200

### ✅ Connected Component Analysis (CCA)

- Implements **8-connectivity** to group connected pixels including diagonals  
- Uses **Union-Find logic** to resolve label collisions efficiently  
- Assigns labels to each region based on intensity match to V-sets  

### ✅ Post-Processing

- **Hole Filling**: Patches gaps in segmented regions  
- **Component Filtering**: Retains only the largest connected components based on pixel frequency  

---

## 📊 Performance Metrics

| Component     | Test Accuracy | Train Accuracy |
|---------------|---------------|----------------|
| Nucleus       | 90.8%         | 88.3%          |
| Cytoplasm     | 97.8%         | 90.1%          |
| WBC Region    | 99.1%         | 98.6%          |
| **Overall**   | **97.75%**    | **95.4%**      |

Metric used: **Dice Coefficient**, defined as:

Dice = (2 × Intersection) / (Sum of Actual + Estimated Pixels)

---

## 🖼️ Segmentation Pipeline

**Step-by-step processing:**

1. Original Image  
2. Local Mean Map  
3. CCA Nucleus  
4. CCA Cytoplasm  
5. Final Segmentation  
6. Ground Truth Mask Comparison  

---

## 🛠️ Implementation Details

### Algorithm Highlights

- **Chunk Size Optimization**: 15×15 blocks balance detection sensitivity and performance  
- **Adaptive Thresholding**: V-set based on local chunk averages  
- **Memory Efficient**: Processes 512×512 images in under 1 second on standard CPUs  

Example V-set configuration:  
- Nucleus range: `range(1, nucleus_mean × 1.1125)`  
- Cytoplasm range: `range(1, overall_mean × 1.025)`

