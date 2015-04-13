# -*- coding: utf-8 -*-

from imposm.parser import OSMParser
import csv


class AddressExtractor:
    def __init__(self, csv_file):
        self.writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.num_addresses = 0

    @staticmethod
    def extract(tags, key):
        value = tags[key] if key in tags else ''
        return value.encode('utf-8')

    def nodes(self, nodes):
        for osmid, tags, refs in nodes:
            if 'addr:city' in tags and 'addr:postcode' in tags and 'addr:street' in tags and 'addr:housenumber' in tags:
                self.num_addresses += 1

                city = self.extract(tags, 'addr:city')
                pc = self.extract(tags, 'addr:postcode')
                street = self.extract(tags, 'addr:street')
                house_number = self.extract(tags, 'addr:housenumber')

                self.writer.writerow([refs[0], refs[1], city, pc, street, house_number])


with open('out-all.csv', 'wb') as csv_file:
    counter = AddressExtractor(csv_file)
    p = OSMParser(concurrency=8, nodes_callback=counter.nodes)
    p.parse('switzerland-latest.osm.pbf')
    print('Found %i addresses.' % counter.num_addresses)
