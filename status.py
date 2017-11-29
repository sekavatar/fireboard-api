from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
import urllib.request
import argparse
import time
import sys
import json


def prettify(elem):
    rough_string = ElementTree.tostring(elem)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="   ", encoding="UTF-8")


def main():
    parser = argparse.ArgumentParser(description='Fireboard Status erzeugen')
    parser.add_argument('--status', dest='status', default='2')
    parser.add_argument('--timestamp', dest='timestamp', default=str(int(time.time())))
    parser.add_argument('--issi', dest='issi', default='')
    parser.add_argument('--opta', dest='opta', default='')
    parser.add_argument('--fmsid', dest='fmsid', default='')
    parser.add_argument('--device_id', dest='device_id', default='')
    parser.add_argument('--apikey', dest='api_key', default='')
    args = parser.parse_args()
    base_uri = 'https://login.fireboard.net/api?authkey=' + args.api_key +\
               '&call=status_data'

    root = Element('fireboardStatus')
    root.set('version', '1.0')

    status_data = SubElement(root, "statusData")
    SubElement(status_data, 'status').text = args.status
    SubElement(status_data, 'issi').text = args.issi
    SubElement(status_data, 'opta').text = args.opta
    SubElement(status_data, 'fms').text = args.fmsid
    SubElement(status_data, 'device_id').text = args.device_id
    timestamp = SubElement(status_data, 'timestamp')
    SubElement(timestamp, 'long').text = args.timestamp

    pret = prettify(root)
    with urllib.request.urlopen(base_uri, data=pret) as response:
        json_response = json.loads(response.read().decode("utf-8"))
        print(json_response)
        if json_response['status'] == 'error':
            print(json_response['errors'])
            return 1
        print("Success!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
