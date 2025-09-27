#!/usr/bin/env python3
"""
Security Anomaly Detection System
Analyzes activity logs to detect suspicious patterns and potential security threats.
"""

import pandas as pd
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import List, Dict, Any, Tuple
import ipaddress

class SecurityAnomalyDetector:
    def __init__(self, csv_file: str):
        """Initialize the detector with log data."""
        self.csv_file = csv_file
        self.df = None
        self.anomalies = []
        self.internal_ip_ranges = [
            ipaddress.IPv4Network('192.168.0.0/16'),
            ipaddress.IPv4Network('10.0.0.0/8'),
            ipaddress.IPv4Network('172.16.0.0/12')
        ]
        
    def load_data(self):
        """Load and preprocess the CSV data."""
        print("Loading and preprocessing data...")
        self.df = pd.read_csv(self.csv_file)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df = self.df.sort_values('timestamp')
        print(f"Loaded {len(self.df)} log entries")
        
    def is_internal_ip(self, ip: str) -> bool:
        """Check if IP is in internal/private range."""
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            return any(ip_obj in network for network in self.internal_ip_ranges)
        except:
            return False
    
    def get_mitigation_suggestions(self, anomaly_type: str, severity: str, details: Dict) -> List[str]:
        """Generate mitigation suggestions based on anomaly type and severity."""
        mitigations = []
        
        if anomaly_type == 'brute_force_attempt':
            mitigations.extend([
                "Block the suspicious IP address immediately",
                "Enable account lockout after 3 failed attempts",
                "Alert security team and investigate the source",
                "Introduce CAPTCHA after multiple failures"
            ])
        elif anomaly_type == 'suspicious_ip':
            mitigations.extend([
                "Block the known suspicious IP address",
                "Add IP to firewall blacklist",
                "Monitor for additional activity from this IP",
                "Alert security team for investigation",
                "Isolate affected systems from the network if compromise is suspected"
            ])
        elif anomaly_type == 'external_ip_access':
            mitigations.extend([
                "Verify user identity through additional authentication",
                "Monitor user activity for suspicious behavior",
                "Consider implementing VPN requirement for external access",
                "Alert user's manager if unusual access pattern"
            ])
        elif anomaly_type == 'geo_hop':
            mitigations.extend([
                "Immediately suspend user account for security review",
                "Force password reset and re-authentication",
                "Alert security team for potential account compromise",
                "Check for unauthorized access to user credentials"
            ])
        elif anomaly_type == 'off_hours_login':
            if severity == 'medium':
                mitigations.extend([
                    "Verify user identity through additional authentication",
                    "Monitor for additional suspicious activity",
                    "Alert user's manager if pattern continues",
                    "Review user role to assess if off-hours activity is expected"
                ])
            else:
                mitigations.extend([
                    "Log the activity for security review",
                    "Monitor for additional off-hours access"
                ])
        elif anomaly_type == 'privilege_escalation':
            mitigations.extend([
                "Immediately suspend the user account",
                "Force password reset and re-authentication",
                "Alert security team for potential account takeover",
                "Review user's recent activity for unauthorized access"
            ])
        elif anomaly_type == 'data_exfiltration':
            mitigations.extend([
                "Immediately suspend user account and network access",
                "Block all download capabilities for the user",
                "Alert security team and management immediately",
                "Preserve all logs and evidence for investigation"
            ])
        
        return mitigations
    
    def detect_brute_force_attempts(self):
        """Detect brute-force login attempts from same IP."""
        print("Detecting brute-force attempts...")
        
        # Group by IP and find consecutive failed logins
        for ip in self.df['ip_address'].unique():
            ip_data = self.df[self.df['ip_address'] == ip].sort_values('timestamp')
            
            failed_attempts = []
            for idx, row in ip_data.iterrows():
                if row['action'] == 'login_failed':
                    failed_attempts.append((row['timestamp'], row['user_id']))
                else:
                    # Check if we have enough failed attempts
                    if len(failed_attempts) >= 3:
                        # Check if all attempts are within 10 minutes
                        time_span = failed_attempts[-1][0] - failed_attempts[0][0]
                        if time_span <= timedelta(minutes=10):
                            anomaly_details = {
                                'attempt_count': len(failed_attempts),
                                'time_span_minutes': time_span.total_seconds() / 60,
                                'affected_users': list(set([attempt[1] for attempt in failed_attempts]))
                            }
                            
                            self.anomalies.append({
                                'timestamp': failed_attempts[0][0].isoformat(),
                                'user_id': failed_attempts[0][1],
                                'ip_address': ip,
                                'anomaly_type': 'brute_force_attempt',
                                'reason': f'Multiple failed login attempts ({len(failed_attempts)}) from same IP within {time_span.total_seconds()/60:.1f} minutes',
                                'severity': 'high',
                                'details': anomaly_details,
                                'mitigation_suggestions': self.get_mitigation_suggestions('brute_force_attempt', 'high', anomaly_details)
                            })
                    failed_attempts = []
            
            # Check final sequence
            if len(failed_attempts) >= 3:
                time_span = failed_attempts[-1][0] - failed_attempts[0][0]
                if time_span <= timedelta(minutes=10):
                    anomaly_details = {
                        'attempt_count': len(failed_attempts),
                        'time_span_minutes': time_span.total_seconds() / 60,
                        'affected_users': list(set([attempt[1] for attempt in failed_attempts]))
                    }
                    
                    self.anomalies.append({
                        'timestamp': failed_attempts[0][0].isoformat(),
                        'user_id': failed_attempts[0][1],
                        'ip_address': ip,
                        'anomaly_type': 'brute_force_attempt',
                        'reason': f'Multiple failed login attempts ({len(failed_attempts)}) from same IP within {time_span.total_seconds()/60:.1f} minutes',
                        'severity': 'high',
                        'details': anomaly_details,
                        'mitigation_suggestions': self.get_mitigation_suggestions('brute_force_attempt', 'high', anomaly_details)
                    })
    
    def detect_suspicious_ips(self):
        """Detect access from suspicious external IPs."""
        print("Detecting suspicious IP addresses...")
        
        suspicious_ips = ['8.8.8.8', '1.1.1.1', '208.67.222.222']  # Common DNS servers
        
        for idx, row in self.df.iterrows():
            ip = row['ip_address']
            
            # Check for known suspicious IPs
            if ip in suspicious_ips:
                anomaly_details = {'ip_type': 'known_suspicious'}
                self.anomalies.append({
                    'timestamp': row['timestamp'].isoformat(),
                    'user_id': row['user_id'],
                    'ip_address': ip,
                    'anomaly_type': 'suspicious_ip',
                    'reason': f'Access from known suspicious IP: {ip}',
                    'severity': 'medium',
                    'details': anomaly_details,
                    'mitigation_suggestions': self.get_mitigation_suggestions('suspicious_ip', 'medium', anomaly_details)
                })
            
            # Check for external IPs only during suspicious activities or off-hours
            elif not self.is_internal_ip(ip):
                # Only flag external IPs during login attempts or off-hours
                if row['action'] in ['login_success', 'login_failed']:
                    hour = row['timestamp'].hour
                    if hour < 8 or hour > 18:  # Off-hours external access
                        anomaly_details = {'ip_type': 'external', 'off_hours': True}
                        self.anomalies.append({
                            'timestamp': row['timestamp'].isoformat(),
                            'user_id': row['user_id'],
                            'ip_address': ip,
                            'anomaly_type': 'external_ip_access',
                            'reason': f'External IP access during off-hours: {ip} at {hour}:00',
                            'severity': 'medium',
                            'details': anomaly_details,
                            'mitigation_suggestions': self.get_mitigation_suggestions('external_ip_access', 'medium', anomaly_details)
                        })
    
    def detect_geo_hops(self):
        """Detect users logging in from very different IP ranges within short time."""
        print("Detecting geo-hops (IP range changes)...")
        
        for user in self.df['user_id'].unique():
            user_data = self.df[self.df['user_id'] == user].sort_values('timestamp')
            
            # Track IP changes over time
            ip_changes = []
            current_ip = None
            current_time = None
            
            for idx, row in user_data.iterrows():
                if row['action'] in ['login_success', 'login_failed']:
                    if current_ip is not None and row['ip_address'] != current_ip:
                        # Check if this is a significant IP range change
                        if self.is_significant_ip_change(current_ip, row['ip_address']):
                            time_diff = row['timestamp'] - current_time
                            if time_diff <= timedelta(hours=2):  # Within 2 hours
                                ip_changes.append({
                                    'timestamp': row['timestamp'],
                                    'from_ip': current_ip,
                                    'to_ip': row['ip_address'],
                                    'time_diff': time_diff
                                })
                    
                    current_ip = row['ip_address']
                    current_time = row['timestamp']
            
            # Flag only significant geo-hops (internal to external or vice versa)
            for change in ip_changes:
                from_internal = self.is_internal_ip(change['from_ip'])
                to_internal = self.is_internal_ip(change['to_ip'])
                
                # Only flag if switching between internal and external networks
                if from_internal != to_internal and change['time_diff'] <= timedelta(minutes=30):
                    anomaly_details = {
                        'from_ip': change['from_ip'],
                        'to_ip': change['to_ip'],
                        'time_diff_minutes': change['time_diff'].total_seconds() / 60,
                        'from_internal': from_internal,
                        'to_internal': to_internal
                    }
                    
                    self.anomalies.append({
                        'timestamp': change['timestamp'].isoformat(),
                        'user_id': user,
                        'ip_address': change['to_ip'],
                        'anomaly_type': 'geo_hop',
                        'reason': f'User switched from {"internal" if from_internal else "external"} to {"internal" if to_internal else "external"} network ({change["from_ip"]} -> {change["to_ip"]}) within {change["time_diff"].total_seconds()/60:.1f} minutes',
                        'severity': 'high',
                        'details': anomaly_details,
                        'mitigation_suggestions': self.get_mitigation_suggestions('geo_hop', 'high', anomaly_details)
                    })
    
    def is_significant_ip_change(self, ip1: str, ip2: str) -> bool:
        """Check if two IPs are from significantly different ranges."""
        try:
            # Extract network portions for comparison
            ip1_network = self.get_ip_network(ip1)
            ip2_network = self.get_ip_network(ip2)
            
            # Different network ranges indicate potential geo-hop
            return ip1_network != ip2_network
        except:
            return False
    
    def get_ip_network(self, ip: str) -> str:
        """Get the network portion of an IP address."""
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            
            # Classify IP into network categories
            if ip_obj in ipaddress.IPv4Network('192.168.0.0/16'):
                return '192.168.x.x'
            elif ip_obj in ipaddress.IPv4Network('10.0.0.0/8'):
                return '10.x.x.x'
            elif ip_obj in ipaddress.IPv4Network('172.16.0.0/12'):
                return '172.16-31.x.x'
            else:
                # External IP - use first two octets
                parts = str(ip_obj).split('.')
                return f"{parts[0]}.{parts[1]}.x.x"
        except:
            return 'unknown'
    
    def detect_off_hours_activity(self):
        """Detect unusual login times (outside business hours) with suspicious patterns."""
        print("Detecting off-hours activity...")
        
        business_hours = (8, 18)  # 8 AM to 6 PM
        
        for idx, row in self.df.iterrows():
            if row['action'] in ['login_success', 'login_failed']:
                hour = row['timestamp'].hour
                if hour < business_hours[0] or hour > business_hours[1]:
                    # Only flag off-hours logins if they're from external IPs or failed attempts
                    is_external = not self.is_internal_ip(row['ip_address'])
                    is_failed = row['action'] == 'login_failed'
                    
                    if is_external or is_failed:
                        severity = 'medium' if is_external else 'low'
                        reason = f'Off-hours login from external IP at {hour}:00' if is_external else f'Failed login attempt at {hour}:00'
                        
                        anomaly_details = {
                            'login_hour': hour,
                            'business_hours': f"{business_hours[0]}-{business_hours[1]}",
                            'external_ip': is_external,
                            'failed_attempt': is_failed
                        }
                        
                        self.anomalies.append({
                            'timestamp': row['timestamp'].isoformat(),
                            'user_id': row['user_id'],
                            'ip_address': row['ip_address'],
                            'anomaly_type': 'off_hours_login',
                            'reason': reason,
                            'severity': severity,
                            'details': anomaly_details,
                            'mitigation_suggestions': self.get_mitigation_suggestions('off_hours_login', severity, anomaly_details)
                        })
    
    def detect_privilege_escalation(self):
        """Detect failed logins followed by successful login (potential password guessing)."""
        print("Detecting potential privilege escalation...")
        
        for user in self.df['user_id'].unique():
            user_data = self.df[self.df['user_id'] == user].sort_values('timestamp')
            
            failed_count = 0
            for idx, row in user_data.iterrows():
                if row['action'] == 'login_failed':
                    failed_count += 1
                elif row['action'] == 'login_success' and failed_count >= 4:
                    # Found successful login after multiple failures
                    anomaly_details = {'failed_attempts_before_success': failed_count}
                    
                    self.anomalies.append({
                        'timestamp': row['timestamp'].isoformat(),
                        'user_id': user,
                        'ip_address': row['ip_address'],
                        'anomaly_type': 'privilege_escalation',
                        'reason': f'Successful login after {failed_count} failed attempts (potential password guessing)',
                        'severity': 'high',
                        'details': anomaly_details,
                        'mitigation_suggestions': self.get_mitigation_suggestions('privilege_escalation', 'high', anomaly_details)
                    })
                    failed_count = 0
                elif row['action'] == 'login_success':
                    failed_count = 0
    
    def detect_data_exfiltration(self):
        """Detect potential data exfiltration (multiple downloads)."""
        print("Detecting potential data exfiltration...")
        
        for user in self.df['user_id'].unique():
            user_data = self.df[self.df['user_id'] == user].sort_values('timestamp')
            downloads = user_data[user_data['action'] == 'download_file']
            
            if len(downloads) >= 8:  # 8 or more downloads
                time_span = downloads.iloc[-1]['timestamp'] - downloads.iloc[0]['timestamp']
                if time_span <= timedelta(hours=1):  # Within 1 hour
                    anomaly_details = {
                        'download_count': len(downloads),
                        'time_span_hours': time_span.total_seconds() / 3600,
                        'download_times': [d['timestamp'].isoformat() for _, d in downloads.iterrows()]
                    }
                    
                    self.anomalies.append({
                        'timestamp': downloads.iloc[0]['timestamp'].isoformat(),
                        'user_id': user,
                        'ip_address': downloads.iloc[0]['ip_address'],
                        'anomaly_type': 'data_exfiltration',
                        'reason': f'User downloaded {len(downloads)} files within {time_span.total_seconds()/3600:.1f} hours',
                        'severity': 'high',
                        'details': anomaly_details,
                        'mitigation_suggestions': self.get_mitigation_suggestions('data_exfiltration', 'high', anomaly_details)
                    })
    
    def run_analysis(self):
        """Run all anomaly detection algorithms."""
        print("Starting security anomaly analysis...")
        print("=" * 50)
        
        self.load_data()
        
        # Run all detection methods
        self.detect_brute_force_attempts()
        self.detect_suspicious_ips()
        self.detect_geo_hops()
        self.detect_off_hours_activity()
        self.detect_privilege_escalation()
        self.detect_data_exfiltration()
        
        print("=" * 50)
        print(f"Analysis complete! Found {len(self.anomalies)} anomalies.")
        
        # Sort anomalies by severity and timestamp
        severity_order = {'high': 3, 'medium': 2, 'low': 1}
        self.anomalies.sort(key=lambda x: (severity_order.get(x['severity'], 0), x['timestamp']), reverse=True)
        
        return self.anomalies
    
    def generate_report(self, output_file: str = 'anomalies_report.json'):
        """Generate JSON report of all anomalies."""
        report = {
            'analysis_metadata': {
                'total_log_entries': len(self.df),
                'analysis_timestamp': datetime.now().isoformat(),
                'total_anomalies_found': len(self.anomalies),
                'anomaly_types': list(set([a['anomaly_type'] for a in self.anomalies])),
                'severity_distribution': dict(Counter([a['severity'] for a in self.anomalies]))
            },
            'anomalies': self.anomalies
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to {output_file}")
        return report

def main():
    """Main function to run the security analysis."""
    detector = SecurityAnomalyDetector('sample_logs_no_status.csv')
    anomalies = detector.run_analysis()
    
    # Generate report
    report = detector.generate_report()
    
    # Print summary
    print("\n" + "=" * 50)
    print("ANOMALY SUMMARY")
    print("=" * 50)
    
    for anomaly in anomalies[:10]:  # Show top 10
        print(f"\n[{anomaly['severity'].upper()}] {anomaly['anomaly_type']}")
        print(f"Time: {anomaly['timestamp']}")
        print(f"User: {anomaly['user_id']}")
        print(f"IP: {anomaly['ip_address']}")
        print(f"Reason: {anomaly['reason']}")
        print("Suggested Mitigations:")
        for i, mitigation in enumerate(anomaly.get('mitigation_suggestions', []), 1):
            print(f"  {i}. {mitigation}")
        print("-" * 30)
    
    if len(anomalies) > 10:
        print(f"\n... and {len(anomalies) - 10} more anomalies (see full report)")

if __name__ == "__main__":
    main()
