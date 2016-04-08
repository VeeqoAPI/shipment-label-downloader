from urllib2 import Request, urlopen
from os.path import abspath, dirname, normpath
from time import strptime
import ConfigParser
import datetime
import json
import sys

CURRENT_PATH = dirname(abspath(__file__))
CONFIG_PATH = normpath('%s/config.ini' % CURRENT_PATH)

configParser = ConfigParser.RawConfigParser()
configParser.read(CONFIG_PATH)
API_KEY = configParser.get('general', 'apikey')

# Default: orders shipped today
UPDATED_AT_MIN = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today()

headers = {
  'Content-Type': 'application/json',
  'x-api-key': API_KEY
}

print 'Retrieving orders shipped at or after %s' % UPDATED_AT_MIN
request = Request('https://api.veeqo.com/orders?page=1&page_size=25&updated_at_min=%s&order_by=created_at&order_direction=desc&status=shipped' % UPDATED_AT_MIN, headers=headers)
response_body = urlopen(request).read()

orders = json.loads(response_body)
for order in orders:
    print 'Checking labels for order %s' % order['number']
    for allocation in order['allocations']:
        if allocation['shipment'] and allocation['shipment']['label_url']:
            # the order can be updated for a number of reasons, but we only
            # need labels for shipped today
            if strptime(allocation['shipment']['created_at'], '%Y-%m-%dT%H:%M:%SZ') > strptime("%s" % UPDATED_AT_MIN, "%Y-%m-%d"):
                print 'Downloading from URL: %s' % allocation['shipment']['label_url']
                label_data = urlopen(allocation['shipment']['label_url']).read()
                label_file_path = normpath("%s/labels/%s-%s.pdf" % (CURRENT_PATH, order['number'], allocation['id']))
                with open(label_file_path, "wb") as label_file:
                    label_file.write(label_data)
