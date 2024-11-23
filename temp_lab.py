import re
from datetime import datetime
import os

# Function to parse a log line


def parse_log_line(line):
    pattern = r'^(\S+) \[(.*?)\] (\S+) (\S+) (\d{3}) (\d+)$'
    match = re.match(pattern, line.strip())
    if match:
        ip_address = match.group(1)
        datetime_str = match.group(2)
        http_method = match.group(3)
        url = match.group(4)
        status_code = int(match.group(5))
        bytes_transferred = int(match.group(6))
        try:
            timestamp = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            timestamp = None
        return {
            'ip_address': ip_address,
            'timestamp': timestamp,
            'http_method': http_method,
            'url': url,
            'status_code': status_code,
            'bytes_transferred': bytes_transferred
        }
    else:
        return None


# Analysis 1: IP Address Analysis

def map_reduce_ip_analysis(log_lines):
    results = {}
    sensitive_urls = ['/admin', '/config']

    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed is None:
            continue
        ip_address = parsed['ip_address']
        status_code = parsed['status_code']
        url = parsed['url']
        success = 1 if 200 <= status_code < 300 else 0

        suspicious = 0
        if status_code in [401, 403] or url in sensitive_urls:
            suspicious = 1

        if ip_address not in results:
            results[ip_address] = {'requests': 0,
                                   'successes': 0, 'suspicious': 0}

        results[ip_address]['requests'] += 1
        results[ip_address]['successes'] += success
        results[ip_address]['suspicious'] += suspicious

    return results


# Analysis 2: Time Window Analysis

def map_reduce_time_window_analysis(log_lines):
    results = {}
    sensitive_urls = ['/admin', '/config']

    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed is None or parsed['timestamp'] is None:
            continue
        timestamp = parsed['timestamp']
        hour = timestamp.strftime('%H:00-%H:59')
        status_code = parsed['status_code']
        url = parsed['url']

        # suspicious = 0
        # if status_code in [401, 403] or url in sensitive_urls:
        # suspicious = 1

        if hour not in results:
            results[hour] = {'requests': 0, 'suspicious': 0}

        results[hour]['requests'] += 1
        # results[hour]['suspicious'] += suspicious

    return results

# Analysis 3: Error Pattern Analysis


def map_reduce_error_pattern_analysis(log_lines):
    error_counts = {}

    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed is None:
            continue
        status_code = parsed['status_code']
        url = parsed['url']
        if status_code >= 400:
            if status_code not in error_counts:
                error_counts[status_code] = {
                    'total_occurrences': 0, 'url_counts': {}}
            error_counts[status_code]['total_occurrences'] += 1
            if url not in error_counts[status_code]['url_counts']:
                error_counts[status_code]['url_counts'][url] = 0
            error_counts[status_code]['url_counts'][url] += 1

    final_results = {}
    for status_code, data in error_counts.items():
        total_occurrences = data['total_occurrences']
        url_counts = data['url_counts']
        top_url = max(url_counts, key=url_counts.get)
        final_results[status_code] = {
            'total_occurrences': total_occurrences,
            'top_url': top_url
        }

    return final_results

# Driver


def driver():
    log_file = 'updated_network.log'
    if not os.path.exists(log_file):
        print(f"Log file '{log_file}' not found in the current directory.")
        return

    with open(log_file, 'r') as file:
        log_lines = file.readlines()

    # Analysis 1: IP Address Analysis
    ip_results = map_reduce_ip_analysis(log_lines)

    print("--- IP Analysis ---")
    for ip, data in sorted(ip_results.items()):
        total_requests = data['requests']
        total_successes = data['successes']
        total_suspicious = data['suspicious']
        success_ratio = (total_successes / total_requests) * \
            100 if total_requests > 0 else 0
        output = f"{ip}: {
            total_requests} requests ({success_ratio:.0f}% success)"
        if total_suspicious > 0:
            output += " [SUSPICIOUS]"
        # if total_requests > 100:
        print(output)

    # Analysis 2: Time Window Analysis
    time_results = map_reduce_time_window_analysis(log_lines)

    max_requests = max((data['requests']
                       for data in time_results.values()), default=0)
    print("\n--- Hourly Analysis ---")
    for hour, data in sorted(time_results.items()):
        total_requests = data['requests']
        output = f"{hour}: {total_requests} requests"
        if total_requests == max_requests and max_requests > 0:
            output += " (peak)"
        if data['suspicious'] > 0:
            output += " [SUSPICIOUS ACTIVITY]"
        print(output)

    # Analysis 3: Error Pattern Analysis
    error_results = map_reduce_error_pattern_analysis(log_lines)

    print("\n--- Error Analysis ---")
    for status_code, data in sorted(error_results.items()):
        total_occurrences = data['total_occurrences']
        top_url = data['top_url']
        output = f"{status_code}: {total_occurrences} occurrences"
        if top_url:
            output += f" (top URL: {top_url})"
        print(output)


if __name__ == "__main__":
    driver()
