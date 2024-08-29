# VISHLESHNAM-Video-Analytics-for-Crowd-Behaviour-Analysis
VISHLESHNAM is an advanced video analytics solution for crowd behaviour analysis using multiple sensors. This project is developed at IIT Bhubaneswar, funded by IRDE Dehradun, DRDO.
Objectives

Develop AI algorithms to detect suspicious activities of intruders targeting women in various environments.
Create AI-driven methodologies for automatic alarm generation to assist women in distress.
Implement vehicle surveillance to detect non-standard or improperly installed number plates within restricted zones.
Develop deep learning models for crowd analysis, including counting males and females and analyzing activities.

Repository Contents

main.py: Core script for video processing, object detection, and database integration.
tracker.py: Implementation of object tracking algorithm.
website.html: Frontend for the project website, including visualizations and user interface.

Setup and Installation

Clone the repository:
Copygit clone https://github.com/your-username/vishleshnam.git

Install required dependencies:
Copypip install -r requirements.txt

Set up the MySQL database as configured in main.py.
Download required model files:

YOLO model: yolov8s.pt
Age and gender models: age_deploy.prototxt, age_net.caffemodel, gender_deploy.prototxt, gender_net.caffemodel


Run the main script:
Copypython main.py


Usage
The system processes video input, detecting and tracking individuals, estimating age and gender, and storing the data in a MySQL database. The web interface (website.html) provides visualizations and analysis of the collected data.
Contributing
We welcome contributions to the VISHLESHNAM project. Please read our contributing guidelines before submitting pull requests
