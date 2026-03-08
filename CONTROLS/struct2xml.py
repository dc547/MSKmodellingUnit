"""Convert a Python nested dictionary into an XML file.

struct2xml(s, file)   - saves to XML file
xml = struct2xml(s)   - returns XML string

A dictionary containing:
    s = {'XMLname': {
        'Attributes': {'attrib1': 'Some value'},
        'Element': {'Text': 'Some text'},
        'DifferentElement': [
            {'Attributes': {'attrib2': '2'}, 'Text': 'Some more text'},
            {'Attributes': {'attrib3': '2', 'attrib4': '1'}, 'Text': 'Even more text'}
        ]
    }}

Will produce:
    <XMLname attrib1="Some value">
      <Element>Some text</Element>
      <DifferentElement attrib2="2">Some more text</DifferentElement>
      <DifferentElement attrib3="2" attrib4="1">Even more text</DifferentElement>
    </XMLname>

Please note that the following strings are substituted:
'_dash_' by '-', '_colon_' by ':' and '_dot_' by '.'

Originally written by W. Falkena, ASTI, TUDelft, 27-08-2010
On-screen output functionality added by P. Orth, 01-12-2010
Multiple space to single space conversion adapted for speed by T. Lohuis, 11-04-2011
Val2str subfunction bugfix by H. Gsenger, 19-9-2011
Modified by Chao-Yuan Yeh, 2016
Python version
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom


def _restore_name(name):
    """Restore special characters from sanitized dict key to XML name."""
    name = name.replace('_dash_', '-')
    name = name.replace('_colon_', ':')
    name = name.replace('_dot_', '.')
    return name


def _val2str(val):
    """Convert a value to its string representation for XML."""
    if val is None:
        return '', True
    if isinstance(val, str):
        return val, True
    if isinstance(val, (int, float)):
        return str(val), True
    return '', False


def _parse_struct(s, parent_element, p_name=''):
    """Recursively convert a dictionary to XML elements.

    Parameters
    ----------
    s : dict
        Dictionary representing the XML structure.
    parent_element : xml.etree.ElementTree.Element
        Parent XML element to append children to.
    p_name : str
        Path name for warning messages.
    """
    for curfield in s:
        curfield_sc = _restore_name(curfield)

        if curfield == 'Attributes':
            # Attribute data
            if isinstance(s[curfield], dict):
                for attr_name, attr_value in s[curfield].items():
                    attr_name_sc = _restore_name(attr_name)
                    txt, success = _val2str(attr_value)
                    if success:
                        parent_element.set(attr_name_sc, txt)
                    else:
                        print(f'Warning. The text in {p_name}{curfield}.{attr_name} could not be processed.')
            else:
                print(f'Warning. The attributes in {p_name}{curfield} could not be processed.')
                print(f"The correct syntax is: {p_name}{curfield}['attribute_name'] = 'Some text'.")

        elif curfield == 'Text':
            # Text data
            txt, success = _val2str(s['Text'])
            if success:
                parent_element.text = txt
            else:
                print(f'Warning. The text in {p_name}{curfield} could not be processed.')

        else:
            # Sub-element
            if isinstance(s[curfield], dict):
                # Single element
                cur_element = ET.SubElement(parent_element, curfield_sc)
                _parse_struct(s[curfield], cur_element, f'{p_name}{curfield}.')
            elif isinstance(s[curfield], list):
                # Multiple elements
                for c, item in enumerate(s[curfield]):
                    cur_element = ET.SubElement(parent_element, curfield_sc)
                    if isinstance(item, dict):
                        _parse_struct(item, cur_element, f'{p_name}{curfield}[{c}].')
                    else:
                        print(f'Warning. The cell {p_name}{curfield}[{c}] could not be processed, since it contains no dict.')
            else:
                # Field contains a plain value; create element with text
                cur_element = ET.SubElement(parent_element, curfield_sc)
                txt, success = _val2str(s[curfield])
                if success:
                    cur_element.text = txt
                else:
                    print(f'Warning. The text in {p_name}{curfield} could not be processed.')


def struct2xml(s, file=None):
    """Convert a nested dictionary into XML.

    Parameters
    ----------
    s : dict
        Nested dictionary with a single root key.
    file : str, optional
        Path to save the XML file. If None, returns XML string.

    Returns
    -------
    str or None
        XML string if file is None, otherwise writes to file.
    """
    if not isinstance(s, dict):
        raise TypeError('Input is not a dictionary')

    keys = list(s.keys())
    if len(keys) != 1:
        raise ValueError('There should be a single field in the main structure.')

    xmlname = keys[0]
    xmlname_sc = _restore_name(xmlname)

    root = ET.Element(xmlname_sc)

    _parse_struct(s[xmlname], root, f'{xmlname}.')

    # Pretty-print the XML
    rough_string = ET.tostring(root, encoding='unicode', xml_declaration=False)
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent='  ', encoding=None)

    # Remove the xml declaration line added by minidom
    lines = pretty_xml.split('\n')
    if lines and lines[0].startswith('<?xml'):
        pretty_xml = '\n'.join(lines[1:])

    # Remove trailing whitespace
    pretty_xml = pretty_xml.strip() + '\n'

    # Add XML declaration at the top
    xml_output = '<?xml version="1.0" encoding="utf-8"?>\n' + pretty_xml

    if file is not None:
        if not file.endswith('.xml'):
            file = file + '.xml'
        with open(file, 'w', encoding='utf-8') as f:
            f.write(xml_output)
    else:
        return xml_output


if __name__ == '__main__':
    import sys
    print("Usage: import struct2xml and call struct2xml(dict_structure, 'output.xml')")
