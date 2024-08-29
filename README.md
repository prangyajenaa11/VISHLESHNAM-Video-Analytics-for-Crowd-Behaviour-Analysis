# VISHLESHNAM-Video-Analytics-for-Crowd-Behaviour-Analysis

## Project Overview

VISHLESHNAM is an advanced video analytics solution for crowd behaviour analysis using multiple sensors. This project aims to develop AI-driven methodologies for detecting suspicious activities, analyzing crowd demographics, and enhancing security measures in various environments.

### Key Features

- AI-based detection of suspicious activities targeting women
- Automatic alarm generation for assisting women in distress
- Vehicle surveillance for detecting non-standard or improperly installed number plates
- Crowd analysis including male/female counting and activity analysis.

## Technical Stack

- **Backend:**
  - Python
  - OpenCV (cv2)
  - YOLO (Ultralytics)
  - MySQL
  - pHp
- **Frontend:**
  - HTML
  - JavaScript
  - CSS

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/vishleshnam.git
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:
   - Create a database named `iitbbsr`
   - Update the database connection details in `main.py`

4. Download the required model files:
   - YOLO model: `yolov8s.pt`
   - Age and Gender models: `age_deploy.prototxt`, `age_net.caffemodel`, `gender_deploy.prototxt`, `gender_net.caffemodel`

5. Run the main script:
   ```
   python main.py
   ```

6. Open `website.html` in a web browser to view the frontend interface.

## Project Structure

- `main.py`: Main script for video processing and analysis
- `tracker.py`: Object tracking implementation
- `website.html`: Frontend interface
- `coco.txt`: COCO dataset class list


