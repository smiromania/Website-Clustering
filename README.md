# 🧠 Logo Similarity Clustering

This project tackles the challenge of grouping websites based on the visual similarity of their logos — without using traditional ML clustering algorithms like K-Means or DBSCAN.

## 🚀 Objective

To extract logos from a list of websites and group them based on how visually similar they are. Logos are crucial elements of brand identity, and being able to automatically detect visual similarity can be useful for analytics, categorization, and brand monitoring.

## 📂 Dataset

The input dataset is a `.parquet` file containing a list of ~4384 website domains in a single column.

## 🧩 Approach

1. **URL Construction**: Domains are transformed into full URLs using HTTPS.
2. **Logo Extraction**:
   - HTML is fetched from each website.
   - The `<link rel="icon">` or similar tags are parsed to identify the logo's URL.
   - Logos are downloaded, resized, and normalized.
3. **Hashing**:
   - Each image is processed using `imagehash.phash`, a perceptual hashing algorithm that captures visual essence.
4. **Grouping**:
   - All logos are compared pairwise.
   - If the Hamming distance between two hashes is below a threshold, the websites are grouped together.

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


