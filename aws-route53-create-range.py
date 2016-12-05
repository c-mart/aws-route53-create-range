#!/usr/bin/python

"""
Creates many zone records in AWS Route 53 that correspond to a range of numeric values.
Prompts interactively for the start and end values of the numeric range, and a pattern for the hostanme and IP address.
Hostnames and IPs are automatically generated and inserted.

Requires the route53 module (`pip install route53`).

Example run:
```
/home/cmart/code/aws-venv/bin/python aws-route53-create-range.py
Enter your AWS access key ID: [redacted]
Enter your AWS access secret key: [redacted]
Enter the name of the zone you wish to update, e.g. 'mydomain.com': cyverse.org
Enter the hostname pattern with underscore as placeholder for number: vm142-_.cyverse.org
Enter the IP address patten with underscore as placeholder for number: 128.196.142._
Enter the start of the numeric range: 2
Enter the end of the numeric range, inclusive: 254

Process finished with exit code 0
```

"""

import route53

aws_access_key_id = raw_input("Enter your AWS access key ID: ")
aws_secret_access_key = raw_input("Enter your AWS access secret key: ")

update_zone_name = raw_input("Enter the name of the zone you wish to update, e.g. 'mydomain.com': ")
if update_zone_name[-1] != ".":
    update_zone_name += "."

hostname_pattern = raw_input("Enter the hostname pattern with underscore as placeholder for number: ")
ip_pattern = raw_input("Enter the IP address patten with underscore as placeholder for number: ")

start_range = int(raw_input("Enter the start of the numeric range: "))
end_range = int(raw_input("Enter the end of the numeric range, inclusive: ")) + 1

conn = route53.connect(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

for zone in conn.list_hosted_zones():
    if zone.name == update_zone_name:
        update_zone_id = zone.id
        break

try:
    update_zone = conn.get_hosted_zone_by_id(update_zone_id)
except NameError as exception:
    print("Could not locate a zone with that name.")
    exit()

for number in range(start_range, end_range):
    hostname = hostname_pattern.replace("_", str(number))
    ip = ip_pattern.replace("_", str(number))
    print("Creating host {0} with value {1}".format(hostname, ip))
    new_record, change_info = update_zone.create_a_record(
        name=hostname,
        values=[ip],
    )
