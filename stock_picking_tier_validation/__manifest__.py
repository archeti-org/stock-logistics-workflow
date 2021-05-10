# Copyright 2021 ArcheTI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Transfer Tier Validation",
    "summary": "Extends the functionality of Transfers to "
    "support a tier validation process.",
    "version": "14.0.1.0.0",
    "category": "Inventory",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "author": "ArcheTI, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["stock", "base_tier_validation"],
    "data": ["views/stock_picking_views.xml"],
}
