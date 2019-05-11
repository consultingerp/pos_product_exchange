# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
##########################################################################
MapId = lambda items:[item.id for item in items]
Mapname = lambda items:[item.name for item in items]
JoinList = lambda item,sep='':'%s'%(sep).join(map(str,item))


DomainVals = lambda domain:dict(map(lambda item :(item[0],item[2]),domain))
IndexItems = lambda items,skey='id':map(lambda item:(item.get(skey),item),items)
ReverseDict =  lambda items:dict((v, k) for k, v in items.items())

def parse_float(item):
    if item and (type(item)==str):
        return float(item.replace(',','') or '0')
    return item

def ensure_string(item):
    return item and item or ' '
def extract_list(obj):
    if isinstance(obj,list) and len(obj):
        obj = obj[0]
    return obj

def extract_item(data,item='value'):
    if isinstance(data,dict):
        return data.get(item) and data.get(item) or data
    return data

def add_text(elem, text):
    elem.text = text

    return elem
def chunks(items, size=10):
    return list(items[i:i+size] for i in xrange(0, len(items), size))

def get_fd(item,f):
    return "{1:.{0}f}".format(f,item)

def prettify(elem):
    from xml.etree import ElementTree
    from xml.dom import minidom
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")
