"""XML2STRUCT converts an XML file into a Python nested dictionary.

outStruct = xml2struct(input)

xml2struct takes either an xml file path or a string in xml format as input
and returns a parsed xml tree as a nested dictionary.

Please note that the following characters are substituted:
'-' by '_dash_', ':' by '_colon_' and '.' by '_dot_'

Originally written by W. Falkena, ASTI, TUDelft, 21-08-2010
Attribute parsing speed increase by 40% by A. Wanner, 14-6-2011
Added CDATA support by I. Smirnov, 20-3-2012
Modified by X. Mo, University of Wisconsin, 12-5-2012
Modified by Chao-Yuan Yeh, August 2016
Python version
"""

import os
import re
import xml.etree.ElementTree as ET


def _sanitize_name(name):
    """Replace special characters to make name safe for use as dict key."""
    name = name.replace('-', '_dash_')
    name = name.replace(':', '_colon_')
    name = name.replace('.', '_dot_')
    return name


def _parse_element(element):
    """Recursively parse an XML element into a nested dictionary."""
    result = {}

    # Parse attributes
    if element.attrib:
        attr_dict = {}
        for attr_name, attr_value in element.attrib.items():
            attr_dict[_sanitize_name(attr_name)] = attr_value
        result['Attributes'] = attr_dict

    # Parse child elements
    children = list(element)
    if children:
        for child in children:
            child_name = _sanitize_name(child.tag)
            child_data = _parse_element(child)

            if child_name in result:
                # XML allows the same elements to be defined multiple times,
                # put each in a different cell (list)
                if not isinstance(result[child_name], list):
                    result[child_name] = [result[child_name]]
                result[child_name].append(child_data)
            else:
                result[child_name] = child_data

    # Parse text content
    text = element.text
    if text is not None:
        stripped = text.strip()
        if stripped:
            result['Text'] = stripped

    # Parse tail text is not needed at this level (handled by parent)

    # If no children, no attributes, and no text, store empty text
    if not result:
        result['Text'] = element.text.strip() if element.text and element.text.strip() else ''

    return result


def xml2struct(xml_input):
    """Convert an XML file or string into a nested dictionary.

    Parameters
    ----------
    xml_input : str
        Path to an XML file or a string containing XML.

    Returns
    -------
    dict
        Nested dictionary representing the XML structure.
    """
    if os.path.isfile(xml_input):
        tree = ET.parse(xml_input)
        root = tree.getroot()
    else:
        try:
            root = ET.fromstring(xml_input)
        except ET.ParseError:
            raise ValueError(
                f"Input is not a valid XML file path or XML string."
            )

    root_name = _sanitize_name(root.tag)
    return {root_name: _parse_element(root)}


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        result = xml2struct(sys.argv[1])
        print(result)
    else:
        print("Usage: python xml2struct.py <xml_file_or_string>")
