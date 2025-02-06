# Dataset Card

---

## Dataset Card for Automatic Pothole Detection System

### Dataset Summary

A curated dataset of real-world road images containing potholes, designed for training object detection models to assist in automated road maintenance and safety management. The project aligns with UN SDGs:
- **3.6**: By 2030, halve the number of global deaths and injuries from road traffic accidents.
- **9.1**: Develop quality, reliable, sustainable, and resilient infrastructure, including regional and transborder infrastructure, to support economic development and human well-being.
- **11.2**: By 2030, provide access to safe, affordable, accessible, and sustainable transport systems for all, improving road safety.

## Dataset Details

### Dataset Description

The aim of this dataset is to support the development of an automated pothole detection system leveraging object detection techniques and real-world data. The dataset is created to:
- Assist authorities in prioritizing road maintenance.
- Reduce accidents.
- Improve urban infrastructure management.

- **Curated by:** [More Information Needed]
- **License:** [More Information Needed]

### Dataset Sources

- **Repository:** [More Information Needed]
- **Paper (optional):** [More Information Needed]
- **Demo (optional):** [More Information Needed]

## Uses

### Direct Use

This dataset is designed for:
- Training and evaluating object detection models for pothole detection.
- Benchmarking different object detection architectures.
- Testing real-world deployment of pothole detection systems.

## Dataset Structure

- **Data Type:** Custom real-world road imagery dataset collected via web scraping, filtered to exclude synthetic and animated images.
- **Sources:**
  - Flickr API
  - DuckDuckGo API
  - Bing API
  - Some pre-cleaned Roboflow datasets (for dummy model creation)

## Dataset Creation

### Source Data

#### Data Collection and Processing

- Data was collected from real-world sources using API-based web scraping.
- Synthetic and animated images were excluded.
- Dataset was processed to ensure high-quality and diverse pothole images.
- Additional cleaning and augmentation techniques were applied.

#### Features and the Target

- **Features:** Real-world road images containing potholes.
- **Target:** Binary classification (pothole or no pothole) or object detection (bounding box around potholes).

### Annotations

#### Annotation Process

- Manual annotation of pothole locations in images.
- Bounding boxes and labels assigned for training object detection models.
- Annotation quality control ensured via multiple passes.

#### Who are the Annotators?

- [More Information Needed]

## Bias, Risks, and Limitations

- The dataset may be biased towards urban roads with higher pothole occurrences.
- Variation in lighting, weather, and road conditions may affect model generalization.
- Ethical considerations must be taken into account when deploying automated road assessment tools.

## Citation (optional)

- If a paper or blog post introducing the dataset is available, APA and BibTeX citations should be included here.



