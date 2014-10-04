#!/usr/bin/python
# -*- coding: utf-8 -*-
import httplib 
import urllib2
import sys
import optparse


def format_url(items_list, regions_list=None, period=None, 
               quantity=None, system=None):

    '''Format the parameters to a URL that will be used by eve-central.

    :param items_list: List of ID for the items you are requesting
    :param regions_list: Restrict statistics to a list of regions
    :param period: Statistics from the last X specified hours
    :param min_qty: The minimum quantity in an order to consider it for the statistics
    :param system: Restrict statistics to a system
    :return: URL
    '''
    
    ENDPOINT = 'http://api.eve-central.com/api/marketstat?'
    params = ''

    for typeid in items_list:
        params += 'typeid=%s&' % typeid

    if regions_list != None:   
        for region in regions_list:
            params += 'regionlimit=%s&' % region    

    if period != None:
        params += 'hours=%s&' % period

    if quantity != None:
        params += 'minQ=%s&' % quantity

    if system != None:
        params += 'usesystem=%s&' % system

    # Remove the last '&'
    params = params[:-1]

    return ENDPOINT + params


def send_request(url):
    ''''''

    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    request.get_full_url()
    request.add_header('User-Agent', 'EVEAppInDevelopment')  
    feed_data = opener.open(request)

    return feed_data.read()


def main(argv):
    ''''''

    parser = optparse.OptionParser()

    parser.add_option('-i', '--item', 
                      help='The type ID of the item(s) you are requesting', 
                      dest='items_list', action='append', type='int')

    parser.add_option('-r', '--region', 
                      help='Restrict statistics to specified region(s)',
                      dest='regions_list', action='append', type='int')

    parser.add_option('-p', '--period', 
                      help='Statistics from the last X specified hours',
                      dest='period')

    parser.add_option('-s', '--system', 
                      help='Restrict statistics to a system', dest='system')

    parser.add_option('-q', '--quantity', 
                      help='The minimum quantity in an order to consider it for the statistics',
                      dest='quantity')

    (opts, args) = parser.parse_args()

    url = format_url(items_list=opts.items_list, 
                     regions_list=opts.regions_list,
                     period=opts.period, 
                     quantity=opts.quantity,
                     system=opts.system)

    data = send_request(url)
    print data


if __name__ == '__main__':
    main(sys.argv[1:])
    
