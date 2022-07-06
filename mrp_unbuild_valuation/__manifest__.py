# Copyright 2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

{
    "name": "Mrp Unbuild Valuation",
    "summary": """
        Module finds and use the cost from account_move_line (stock valuation layer -> move line)
         from the MO linked to Unbilled Order""",
    "version": "15.0.1.0.0",
    "category": "Uncategorized",
    "website": "http://sodexis.com/",
    "author": "Sodexis",
    "license": "OPL-1",
    "installable": True,
    "application": False,
    "depends": [
        "mrp",
    ],
    "data": [],
}
