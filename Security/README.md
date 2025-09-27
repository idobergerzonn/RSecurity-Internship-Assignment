# Security Anomaly Detection System

## Overview
A Python-based system that analyzes activity logs to detect suspicious patterns and potential security threats. Processes CSV log files and identifies various types of anomalies that could indicate malicious behavior.

## Detection Approach

The system uses **rule-based pattern recognition** with multiple detection algorithms:

### Core Detection Methods
1. **Brute Force Detection**: Detected multiple (3 or more) failed login attempts from the same IP address within 10 minutes, indicating a potential brute-force attack.
2. **Suspicious IP Detection**: Login activity was observed from a known suspicious IP (e.g., public DNS servers like 8.8.8.8) that should not be used for authentication.
3. **external_ip_access**: A login attempt was made from an external IP address (outside private/internal ranges) during non-business hours, raising suspicion of unauthorized access.
4. **Geo-hop Detection**: A user switched between significantly different IP ranges (e.g., internal to external) within a short time window, suggesting a possible VPN usage or location spoofing.
5. **Privilege Escalation**: A successful login was preceded by multiple failed attempts, possibly indicating a successful password guessing or account compromise.
6. **Data Exfiltration**: A user downloaded 8 or more files within 1 hour, potentially signaling data exfiltration or unauthorized bulk access.
7. **Off-hours Activity**: An entry is flagged as an anomaly if a user attempts to log in (either login_success or login_failed) outside of business hours (before 8:00 AM or after 6:00 PM), and one of the following is true:
The login comes from an external IP address → flagged as medium severity.
OR
The login attempt fails, regardless of IP type → flagged as low severity.


### Technical Implementation
- **Time-based Analysis**: Sliding window algorithms for temporal pattern detection
- **IP Network Analysis**: Uses Python's `ipaddress` module for network range classification
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
├── anomaly_analysis_dashboard.png # Visual dashboard
└── requirements.txt              # Dependencies
```

## Dependencies
- `pandas>=1.3.0`: Data processing
- `ipaddress`: IP network analysis
- `matplotlib`: Visualization

## Sample Results
From 416 log entries, the system typically detects:
- **215 total anomalies** (11 high-severity, 204 medium-severity)
- **1 brute force attack** from external IP
- **10 privilege escalation** attempts
- **Multiple geo-hops** and external IP access patterns

## Security Features
- **Offline Analysis**: No external network calls
- **Local Processing**: All data processed locally
- **Comprehensive Coverage**: Multiple attack vector detection
- **Visual Analytics**: Charts and statistical summaries