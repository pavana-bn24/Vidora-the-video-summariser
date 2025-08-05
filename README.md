# 🎬 Vidora - Smart Video Summarization Tool

**Vidora** is a lightweight, AI-powered video summarizer that helps users get the essence of lengthy videos within seconds. Designed for productivity and efficiency, Vidora scans through content to deliver meaningful highlights and summaries — ideal for lectures, tutorials, interviews, and more.

---

## 🧠 What It Does

- Extracts key scenes and spoken content from videos  
- Summarizes them into a short, understandable format  
- Saves your time by skipping unnecessary parts

Whether you're reviewing a 2-hour lecture or catching up on a missed webinar, Vidora makes it quick and effective.

---

## 💼 Use Case Examples

- Students revising entire lectures in under 2 minutes  
- Professionals scanning webinars and talks  
- Creators repurposing long content into bite-sized clips  
- Language learners simplifying native-language videos

---

## 🔧 Tech Stack (Backend Focused)

- **Language:** Python  
- **Key Libraries:** `moviepy`, `transformers`, `scikit-learn`, `nltk`  
- **Video Handling:** FFmpeg / OpenCV  
- **Text Analysis:** HuggingFace transformers, TextRank or custom NLP models

---

## ⚙️ How to Run (Example)

```bash
# Step 1: Unzip the backend project
unzip vidora-backend.zip
cd vidora-backend

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the main script
python main.py --input "your_video_file.mp4"
