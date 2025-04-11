# 🧠 Logo Similarity Clustering

This project tackles the challenge of grouping websites based on the visual similarity of their logos — without using traditional ML clustering algorithms like K-Means or DBSCAN.

## 🚀 Objective

To extract logos from a list of websites and group them based on how visually similar they are. Logos are crucial elements of brand identity, and being able to automatically detect visual similarity can be useful for analytics, categorization, and brand monitoring.

## 📂 Dataset

The input dataset is a `.parquet` file containing a list of ~4384 website domains in a single column.

## 🧩 Approach

This undertaking displays the design of the anticipated productive deliverables:

### ✅ Solution Exposition / Presentation
From my side, I looked at this as a task of visual hash and comparison. Instead of K-Means or DBSCAN, I used perceptual hashing to quantify the visual similarity between logos. The idea was to keep it low-tech and deterministic, and to scale up for an efficient performance on small to mid-size datasets.

We played around with different icon tags-such as

`<link rel="icon">`,`apple-touch-icon`, and what not-before finally deciding on hash, which gave the intewriting and consistent outputs. It provides clarity and simplicity but still possesses strong accuracy.

### 📊 Output
- Over **97% of the websites** have logos extracted from more than 4300 domains. Only **2 Failures** were recorded while extracting the logos.
- The script generates multiple groups of websites that share similar logos.
- Some logos were unique and resulted in single-entry groups, which is expected. Or they were to small resolution to be compared with the average resolution images.
- The only known mis-clusterings occurred where logos were of a really low resolution.

The output contains a grouped list of domains and can be exported as JSON or printed directly.

### 🧠 Code and Logic
It is thus the full Python implementation of this repository which takes any.parquet file with website domains, constructs URLs automatically, gets logos, hashes them, and groups similar logos together. It can be run against datasets of any size, is robust, and is clear.

## ✅ Results

- Logos were successfully extracted from **all but 2 websites** in the dataset.
- The algorithm grouped logos with a high accuracy.
- The only notable grouping errors occurred in cases where logo images were **extremely low resolution**, making their hash signatures unreliable, making them single-element groups.
- We can get even less groups if we are to choose lowering the **threshold**.

## Technologies Used

- Python 3
- `pandas` for data handling
- `requests` for HTTP requests
- `beautifulsoup4` for HTML parsing
- `Pillow` for image manipulation
- `imagehash` for perceptual hashing

## Expected Output

The output consists of multiple groups (lists of domains), each representing websites that share visually similar logos.


