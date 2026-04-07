"""Generate a mihomo-compatible IP-CIDR ruleset from Discord IP lists.

Reads voice-ip-list.txt and base-ip-list.txt, deduplicates, and outputs
a YAML file with each IP as an individual /32 rule for precise matching.
"""

import os
import re


def alphanumeric_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


def read_ips(filepath):
    """Read IPs from a text file, one per line."""
    if not os.path.isfile(filepath):
        print(f"Warning: {filepath} not found, skipping.")
        return set()
    with open(filepath, 'r') as f:
        return {line.strip() for line in f if line.strip()}


def main():
    data_dir = "data"
    voice_ips = read_ips(os.path.join(data_dir, "voice-ip-list.txt"))
    base_ips = read_ips(os.path.join(data_dir, "base-ip-list.txt"))

    all_ips = sorted(voice_ips | base_ips, key=alphanumeric_key)
    print(f"Total unique IPs: {len(all_ips)}")

    output_path = os.path.join(data_dir, "mihomo-discord-ip.yaml")
    with open(output_path, 'w') as f:
        f.write("payload:\n")
        for ip in all_ips:
            f.write(f"  - '{ip}/32'\n")

    print(f"Written to {output_path}")


if __name__ == "__main__":
    main()
