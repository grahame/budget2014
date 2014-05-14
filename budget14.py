#!/usr/bin/env python3

from lxml import etree
etree.set_default_parser(etree.HTMLParser())
import os
import subprocess
import requests
from urllib.parse import urljoin
from io import BytesIO

tmpdir = './tmp/'
indexes = [
    'http://www.budget.gov.au/2014-15/content/bp1/html/index.htm',
    'http://www.budget.gov.au/2014-15/content/bp2/html/index.htm',
    'http://www.budget.gov.au/2014-15/content/bp3/html/index.htm',
    'http://www.budget.gov.au/2014-15/content/bp4/html/index.htm' ]
chunk_size = 4096

def main():
    pdfs = []
    for index_uri in indexes:
        print("up to:", index_uri)
        data = requests.get(index_uri).content
        et = etree.parse(BytesIO(data))
        for elem in et.xpath('//a[contains(@href, ".pdf")]'):
            idx = len(pdfs)
            pdf = os.path.join(tmpdir, '%d.pdf' % (idx))
            pdfs.append(pdf)
            tmpf = pdf + '_tmp'
            if os.access(pdf, os.R_OK):
                print("skipping %d, already down..." % (idx))
                continue
            print("getting:", pdf)
            req = requests.get(urljoin(index_uri, elem.get('href')), stream=True)
            with open(tmpf, 'wb') as fd:
                for data in req.iter_content(chunk_size):
                    fd.write(data)
                os.rename(tmpf, pdf)
    cmd = [ 'pdftk' ] + pdfs + ['cat', 'output', 'budget2014.pdf']
    print(cmd)
    subprocess.call(cmd)

if __name__ == '__main__':
    main()


