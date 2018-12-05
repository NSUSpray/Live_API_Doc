# -*- coding: utf-8 -*-
import sys, re, codecs
import xml.etree.ElementTree as ET

reload (sys)
sys.setdefaultencoding ('utf-8')


old_filename = sys.argv [1]
new_filename = sys.argv [2]
dest_filename = old_filename.replace ('.xml', '-') + new_filename.replace ('Live', '') if len (sys.argv) < 4 else sys.argv [3]
old_doc = ET.ElementTree (file=old_filename)
new_doc = ET.ElementTree (file=new_filename)
primary = old_doc.getroot ()
target = new_doc.getroot ()
primary.set ('version', primary.get ('version') + '-' + target.get ('version'))


def without_listener_fix__device_and_chain_first (elem):
    text = elem.get ('name')
    if text.endswith ('()'): text = text [:-2]
    if elem.tag == 'Module':
        text = re.compile('([A-Z][a-zA-Z0-9]*)Device').sub (r'Device!\1 ', text)
        text = re.compile('([A-Z][a-zA-Z0-9]*)Chain').sub (r'Chain!\1 ', text)
    elif elem.tag == 'Method':
        text = re.compile('add_(.*)_listener').sub (r'\1 ', text)
        text = re.compile('remove_(.*)_listener').sub (r'\1 ', text)
        text = re.compile('(.*)_has_listener').sub (r'\1 ', text)
    return text

def in_order (a_elem, b_elem):
    return without_listener_fix__device_and_chain_first (a_elem) < without_listener_fix__device_and_chain_first (b_elem)

def apply_compare (primary, target):
    added = deleted = common = changed = False
    
    primary_children = primary.getchildren ()
    target_children = target.getchildren ()
    
    primary_docs = [child for child in primary_children if child.tag == 'Doc']
    target_docs = [child for child in target_children if child.tag == 'Doc']
    primary_tptxs = [[doc.get ('type'), doc.text] for doc in primary_docs]
    target_tptxs = [[doc.get ('type'), doc.text] for doc in target_docs]
    ###########################################################################
    added_tptxs = [tptx for tptx in target_tptxs if tptx not in primary_tptxs]
    if added_tptxs:
        added_docs = [doc for doc in target_docs if [doc.get ('type'), doc.text] in added_tptxs]
        for added_doc in added_docs:
            added_doc.set ('compare', 'added changed')
            # insert after last same-type doc
            same_primary_docs = [doc for doc in primary_docs if doc.get ('type') == added_doc.get ('type')]
            if same_primary_docs:
                prev_doc = same_primary_docs [-1]
                prev_doc_index = primary_children.index (prev_doc)
                primary.insert (prev_doc_index + 1, added_doc)
            else:
                primary.append (added_doc)
            if added_doc.get ('type') != 'Cpp-Signature':
                changed = True
    ###########################################################################
    deleted_tptxs = [tptx for tptx in primary_tptxs if tptx not in target_tptxs]
    if deleted_tptxs:
        deleted_docs = [doc for doc in primary_docs if [doc.get ('type'), doc.text] in deleted_tptxs]
        for deleted_doc in deleted_docs:
            deleted_doc.set ('compare', 'deleted changed')
            if deleted_doc.get ('type') != 'Cpp-Signature':
                changed = True
    ###########################################################################
    #common_tptxs = [tptx for tptx in target_tptxs if tptx in primary_tptxs]
    #if common_tptxs:
    #    common_docs = [doc for doc in primary_docs if [doc.get ('type'), doc.text] in common_tptxs]
    #    for common_doc in common_docs:
    #        common_doc.set ('compare', 'common')
    #    common = True
    
    primary_members = [child for child in primary_children if child.tag != 'Doc']
    target_members = [child for child in target_children if child.tag != 'Doc']
    primary_names = [member.get ('name') for member in primary_members]
    target_names = [member.get ('name') for member in target_members]
    ###########################################################################
    added_names = [name for name in target_names if name not in primary_names]
    if added_names:
        added_members = [member for member in target_members if member.get ('name') in added_names]
        for added_member in added_members:
            added_member.set ('compare', 'added')
            # insert after last same-name member
            next_primary_members = [member for member in primary_members if in_order (added_member, member)]
            if next_primary_members:
                next_member = next_primary_members [0]
                next_member_index = primary_children.index (next_member)
                primary.insert (next_member_index, added_member)
            else:
                primary.insert (len (primary_children), added_member)
        added = True
    ###########################################################################
    deleted_names = [name for name in primary_names if name not in target_names]
    if deleted_names:
        deleted_members = [member for member in primary_members if member.get ('name') in deleted_names]
        for deleted_member in deleted_members:
            deleted_member.set ('compare', 'deleted')
        deleted = True
    ###########################################################################
    common_names = [name for name in target_names if name in primary_names]
    if common_names:
        primary_common_members = [member for member in primary_members if member.get ('name') in common_names]
        target_common_members = [member for member in target_members if member.get ('name') in common_names]
        common_members_pairs = zip (primary_common_members, target_common_members)
        for primary_member, target_member in common_members_pairs:
            primary_member.set ('compare', 'common')
            _added, _deleted, _changed = apply_compare (primary_member, target_member)
            if _added: added = True
            if _deleted: deleted = True
            if _changed: changed = True
        common = True
    
    if primary.get ('compare') == 'common':
        common = True
    
    compare = added * ' added' + changed * ' changed' + deleted * ' deleted' + common * ' common'
    if compare:
        compare = compare [1:] # cut first space
        primary.set ('compare', compare)
    return [added, deleted, changed]


apply_compare (primary, target)

dest_doc = ET.ElementTree (primary)


with open (dest_filename, 'w') as dest_file:
    dest_file.write (codecs.BOM_UTF8)
    dest_file.write ('<?xml version="1.0" encoding="utf-8"?>')
    dest_file.write ('<?xml-stylesheet type="text/xsl" href="LiveAPI.xsl"?>')
    dest_doc.write (dest_file, 'utf-8')
