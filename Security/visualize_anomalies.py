#!/usr/bin/env python3
"""
Simple visualization script for anomaly analysis results
"""

import json
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from datetime import datetime

def load_anomalies_report(filename='anomalies_report.json'):
    """Load the anomalies report."""
    with open(filename, 'r') as f:
        return json.load(f)

def create_visualizations(report):
    """Create various visualizations of the anomaly data."""
    
    anomalies = report['anomalies']
    df = pd.DataFrame(anomalies)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create subplots with better spacing
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Security Anomaly Analysis Dashboard', fontsize=16, fontweight='bold')
    plt.subplots_adjust(hspace=0.3, wspace=0.3)  # Add more space between subplots
    
    # 1. Anomaly types distribution - Use horizontal bar chart for better readability
    anomaly_counts = Counter([a['anomaly_type'] for a in anomalies])
    
    # Sort by count for better visualization
    sorted_anomalies = dict(sorted(anomaly_counts.items(), key=lambda x: x[1], reverse=True))
    
    # Create horizontal bar chart instead of pie chart
    bars = axes[0, 0].barh(list(sorted_anomalies.keys()), list(sorted_anomalies.values()))
    axes[0, 0].set_title('Anomaly Types Distribution', fontsize=10, fontweight='bold')
    axes[0, 0].set_xlabel('Count', fontsize=9)
    
    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, sorted_anomalies.values())):
        axes[0, 0].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                       f'{count}', ha='left', va='center', fontsize=8, fontweight='bold')
    
    # Rotate y-axis labels for better readability
    axes[0, 0].tick_params(axis='y', labelsize=8)
    
    # 2. Severity distribution
    severity_counts = Counter([a['severity'] for a in anomalies])
    colors = {'high': 'red', 'medium': 'orange', 'low': 'yellow'}
    axes[0, 1].bar(severity_counts.keys(), severity_counts.values(), 
                   color=[colors[s] for s in severity_counts.keys()])
    axes[0, 1].set_title('Severity Distribution')
    axes[0, 1].set_ylabel('Count')
    
    # 3. Anomalies over time (daily)
    df['date'] = df['timestamp'].dt.date
    daily_counts = df.groupby('date').size()
    axes[1, 0].plot(daily_counts.index, daily_counts.values, marker='o')
    axes[1, 0].set_title('Anomalies Over Time (Daily)')
    axes[1, 0].set_xlabel('Date')
    axes[1, 0].set_ylabel('Anomaly Count')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Top users with anomalies
    user_counts = Counter([a['user_id'] for a in anomalies])
    top_users = dict(user_counts.most_common(10))
    axes[1, 1].bar(range(len(top_users)), list(top_users.values()))
    axes[1, 1].set_title('Top 10 Users with Anomalies')
    axes[1, 1].set_xlabel('Users')
    axes[1, 1].set_ylabel('Anomaly Count')
    axes[1, 1].set_xticks(range(len(top_users)))
    axes[1, 1].set_xticklabels(list(top_users.keys()), rotation=45)
    
    plt.tight_layout()
    plt.savefig('anomaly_analysis_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close the plot instead of showing it
    
    # Only print a short success message
    print(f"✓ Visualization completed successfully! Dashboard saved as 'anomaly_analysis_dashboard.png'")
    print(f"  Processed {len(anomalies)} anomalies from {len(set(a['user_id'] for a in anomalies))} users")

def main():
    """Main function to run visualizations."""
    try:
        report = load_anomalies_report()
        create_visualizations(report)
    except FileNotFoundError:
        print("Error: anomalies_report.json not found. Run detect_anomalies.py first.")
    except ImportError:
        print("Error: matplotlib not installed. Install with: pip install matplotlib")

if __name__ == "__main__":
    main()
