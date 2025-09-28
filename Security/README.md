# Security Anomaly Detection System

## Overview
A Python-based system that analyzes activity logs to detect suspicious patterns and potential security threats. Processes CSV log files and identifies various types of anomalies that could indicate malicious behavior.

## Detection Approach

The system uses **rule-based pattern recognition** combined with **machine learning** for comprehensive anomaly detection:

### Core Detection Methods
1. **Brute Force Detection**: Detected multiple (3 or more) failed login attempts from the same IP address within 10 minutes, indicating a potential brute-force attack.
2. **Suspicious IP Detection**: Login activity was observed from a known suspicious IP (e.g., public DNS servers like 8.8.8.8) that should not be used for authentication.
3. **external_ip_access**: A login attempt was made from an external IP address (outside private/internal ranges) during non-business hours, raising suspicion of unauthorized access.
4. **Geo-hop Detection**: A user switched between significantly different IP ranges (e.g., internal to external) within a short time window, suggesting a possible VPN usage or location spoofing.
5. **Privilege Escalation**: A successful login was preceded by multiple failed attempts, possibly indicating a successful password guessing or account compromise.
6. **Off-hours Activity**: An entry is flagged as an anomaly if a user attempts to log in (either login_success or login_failed) outside of business hours (before 8:00 AM or after 6:00 PM), and one of the following is true:
The login comes from an external IP address → flagged as medium severity.
OR
The login attempt fails, regardless of IP type → flagged as low severity.
7. **ML Anomaly Detection**: Uses Isolation Forest machine learning algorithm to identify unusual patterns in user behavior based on timing, action types, and IP addresses.


### Technical Implementation
- **Time-based Analysis**: Sliding window algorithms for temporal pattern detection
- **IP Network Analysis**: Uses Python's `ipaddress` module for network range classification
- **Machine Learning**: Isolation Forest algorithm for unsupervised anomaly detection
- **Feature Engineering**: Converts timestamps, actions, and IP addresses into ML-compatible features
- **Severity Classification**: High/Medium/Low based on threat level
- **Statistical Processing**: Pandas for efficient data manipulation and grouping

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Usage
```bash
# Run analysis
python detect_anomalies.py

# Generate visualizations
python visualize_anomalies.py
```

### Output
- **Console**: Top 10 anomalies summary
- **anomalies_report.json**: Complete structured report
- **anomaly_analysis_dashboard.png**: Visual dashboard with charts

## Input Format
CSV file with columns: `timestamp`, `user_id`, `action`, `ip_address`


## Project Structure
```
Security/
├── detect_anomalies.py           # Main detection script
├── visualize_anomalies.py        # Visualization generator
├── sample_logs_no_status.csv     # Input data
├── anomalies_report.json         # Analysis results
└── requirements.txt              # Dependencies
```

## Dependencies


- `pandas>=1.3.0`: Data processing and analysis
- `scikit-learn>=1.0.0`: Machine learning algorithms (Isolation Forest)
- `matplotlib>=3.5.0`: Data visualization and dashboard generation
- `ipaddress`: IP network analysis 
