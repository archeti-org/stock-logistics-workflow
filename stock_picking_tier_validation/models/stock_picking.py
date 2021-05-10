# Copyright 2021 ArcheTI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import ValidationError


class Picking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "tier.validation"]
    _state_from = ["draft", "waiting", "confirmed", "assigned"]
    _state_to = ["done"]

    _tier_validation_manual_config = False

    def button_validate(self):
        return super(
            Picking, self.with_context(validate_in_progress=True)
        ).button_validate()

    def write(self, vals):
        """
        Overwritten to call some custom methods for the tier validation process
        since field state is a computed one, and base code in tier_validation
        does not work as expected, when the state is 'done'
        """
        for rec in self:
            if rec._check_state_conditions_custom():
                if rec._get_need_validation():
                    # try to validate operation
                    reviews = rec.request_validation()
                    rec._validate_tier(reviews)
                    if not self._calc_reviews_validated(reviews):
                        raise ValidationError(
                            _(
                                "This action needs to be validated for at"
                                " least one record. \nPlease request a"
                                " validation."
                            )
                        )
                if rec.review_ids and not rec.validated:
                    raise ValidationError(
                        _(
                            "A validation process is still open for at least "
                            "one record."
                        )
                    )
        return super(Picking, self).write(vals)

    def _check_state_conditions_custom(self):
        """
        Needed because state is a computed field,
        _check_state_conditions in model tier_validation, does not work
        when the state is 'done'
        """
        self.ensure_one()
        if self._context.get("validate_in_progress"):
            return True
        return False

    def _get_need_validation(self):
        """
        Needed because state is a computed field,
        _compute_need_validation (field need_validation) in model
        tier_validation, does not properly works when executing button
        "Validate"
        """
        self.ensure_one()
        if isinstance(self.id, models.NewId):
            return False
        tiers = self.env["tier.definition"].search([("model", "=", self._name)])
        valid_tiers = any([self.evaluate_tier(tier) for tier in tiers])
        return (
            not self.review_ids
            and valid_tiers
            and self._context.get("validate_in_progress")
        )
