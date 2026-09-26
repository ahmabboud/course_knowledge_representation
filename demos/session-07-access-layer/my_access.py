"""Session 7 lab, part B, task Y2: make the check catch invented classes.

access_layer.unknown_properties catches a property the graph does not have
(ul:shippedBy). A model can also invent a class (ul:Shipment, ul:Warehouse).
Write unknown_classes: the twin of unknown_properties, for classes.

Copy unknown_properties from access_layer.py and change three things:
  classes instead of props; t[0].isupper() instead of t[0].islower();
  "class" instead of "property" in the message.

Then:  python check_my_access.py
And see what it changes:  python evaluate.py --setting repair --add-class-check
"""

from access_layer import ul_terms  # noqa: F401  (you will need it)


def unknown_classes(query, classes, props):
    """Problems: ul: classes the query uses that the graph does not have."""
    # TODO: copy unknown_properties from access_layer.py and change it for classes
    raise NotImplementedError
