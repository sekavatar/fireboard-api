from xml.etree.ElementTree import Element, SubElement
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
    parser = argparse.ArgumentParser(description='Fireboard Einsatz erzeugen')
    parser.add_argument('--external_number', dest='external_number', default='')  # a.k.a. Leitstellennummer
    parser.add_argument('--uniqueid', dest='unique_id', default=str(int(time.time())))
    parser.add_argument('--keyword', dest='keyword', default='')
    parser.add_argument('--announcement', dest='announcement', default='')
    parser.add_argument('--location', dest='location', default='')
    parser.add_argument('--latitude', dest='latitude', default='')
    parser.add_argument('--longitude', dest='longitude', default='')
    parser.add_argument('--timestamp', dest='timestamp', default='')
    parser.add_argument('--situation', dest='situation', default='')
    parser.add_argument('--apikey', dest='api_key', default='')
    args = parser.parse_args()
    base_uri = 'https://login.fireboard.net/api?authkey=' + args.api_key + '&call=operation_data'

    root = Element('fireboardOperation')
    root.set('version', '1.0')
    SubElement(root, 'uniqueId').text = args.unique_id

    basic_data = SubElement(root, "basicData")
    SubElement(basic_data, 'externalNumber').text = args.external_number
    SubElement(basic_data, 'keyword').text = args.keyword
    SubElement(basic_data, 'announcement').text = args.announcement
    SubElement(basic_data, 'location').text = args.location
    geo_location = SubElement(basic_data, 'geo_location')
    SubElement(geo_location, 'latitude').text = args.latitude
    SubElement(geo_location, 'longitude').text = args.longitude
    timestamp_started = SubElement(basic_data, 'timestampStarted')
    SubElement(timestamp_started, 'long').text = args.timestamp
    SubElement(basic_data, 'situation').text = args.situation

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
