# Exploration of Vietnam Administrative Subdivision WebService

Inspired by the [dvhcvn repo by daohoangson](https://github.com/daohoangson/dvhcvn), but at the same time can't understand PHP, this is a python implementation of retrieving and outputting Vietnam's Administrative Subdivision WebService into a json format that's easier for web consumption.

# Use of resulting data
Interested users should download or use directly:

- [provinces.json](provinces.json)
- [districts.json](districts.json)
- [wards.json](wards.json)

# Retrieve your own data
Since Vietnam's administrative subdivisions are surprisingly dynamic [given how often there are changes](https://danhmuchanhchinh.gso.gov.vn/NghiDinh.aspx), it might be better to automate retrieiving your own data.

The script, [retrieving_subdivisions.py](retrieving_subdivisions.py), is very simple. It creates a `request` with the most expansive parameters to all three webservices provided regarding provinces, districts, and wards, then parse and output the json accordingly.

Usage is as simple as:

```bash
$ python3 retrieving_subdivisions.py
```

## Dependencies
Usage of the `requests`, `datetime`, `xmltodict`, and `json` libraries

