from typing import Any


def create_rule_result(
    rule_id: str,
    field: str,
    status: str,
    message: str,
    weight: int,
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "field": field,
        "status": status,
        "message": message,
        "weight": weight,
    }


def check_product_name(
    fields: dict[str, Any],
) -> dict[str, Any]:
    value = fields.get("product_name")

    if value:
        return create_rule_result(
            "LM-PC-001",
            "product_name",
            "PASS",
            "Product name was successfully identified.",
            17,
        )

    return create_rule_result(
        "LM-PC-001",
        "product_name",
        "NOT_VERIFIABLE",
        "Product name could not be identified from the available label information.",
        17,
    )


def check_mrp(
    fields: dict[str, Any],
) -> dict[str, Any]:
    value = fields.get("mrp")

    if value is not None:
        return create_rule_result(
            "LM-PC-002",
            "mrp",
            "PASS",
            f"MRP value identified as ₹{value}.",
            18,
        )

    return create_rule_result(
        "LM-PC-002",
        "mrp",
        "NOT_VERIFIABLE",
        "MRP label was detected, but a numeric MRP value could not be reliably extracted.",
        18,
    )


def check_net_quantity(
    fields: dict[str, Any],
) -> dict[str, Any]:
    value = fields.get("net_quantity_value")
    unit = fields.get("net_quantity_unit")

    if value is not None and unit:
        return create_rule_result(
            "LM-PC-003",
            "net_quantity",
            "PASS",
            f"Net quantity identified as {value} {unit}.",
            17,
        )

    return create_rule_result(
        "LM-PC-003",
        "net_quantity",
        "NOT_VERIFIABLE",
        "Net quantity could not be reliably extracted.",
        17,
    )


def check_manufacturer(
    fields: dict[str, Any],
) -> dict[str, Any]:
    value = fields.get("manufacturer")

    if value:
        return create_rule_result(
            "LM-PC-004",
            "manufacturer",
            "PASS",
            "Manufacturer or responsible entity information was identified.",
            10,
        )

    return create_rule_result(
        "LM-PC-004",
        "manufacturer",
        "NOT_VERIFIABLE",
        "Manufacturer or responsible entity information could not be identified.",
        10,
    )


def check_date_information(
    fields: dict[str, Any],
) -> dict[str, Any]:
    manufacturing_date = fields.get(
        "manufacturing_date"
    )

    packing_date = fields.get(
        "packing_date"
    )

    best_before = fields.get(
        "best_before"
    )

    use_by = fields.get(
        "use_by"
    )

    if (
        manufacturing_date
        or packing_date
        or best_before
        or use_by
    ):
        return create_rule_result(
            "LM-PC-007",
            "date_information",
            "PASS",
            "Relevant date or shelf-life information was identified.",
            18,
        )

    return create_rule_result(
        "LM-PC-007",
        "date_information",
        "NOT_VERIFIABLE",
        "Manufacturing, packing, best-before or use-by information could not be reliably identified.",
        18,
    )


def check_consumer_care(
    fields: dict[str, Any],
) -> dict[str, Any]:
    value = fields.get(
        "consumer_care_details"
    )

    if value:
        return create_rule_result(
            "LM-PC-008",
            "consumer_care_details",
            "PASS",
            "Consumer care/contact information was identified.",
            10,
        )

    return create_rule_result(
        "LM-PC-008",
        "consumer_care_details",
        "NOT_VERIFIABLE",
        "Consumer care/contact information could not be reliably extracted.",
        10,
    )


def check_country_of_origin(
    fields: dict[str, Any],
) -> dict[str, Any]:
    value = fields.get(
        "country_of_origin"
    )

    if value:
        return create_rule_result(
            "LM-PC-009",
            "country_of_origin",
            "PASS",
            f"Country of origin identified as {value}.",
            10,
        )

    return create_rule_result(
        "LM-PC-009",
        "country_of_origin",
        "NOT_VERIFIABLE",
        "Country of origin was not identified. Applicability depends on the product/category.",
        10,
    )


def evaluate_compliance(
    fields: dict[str, Any],
) -> dict[str, Any]:
    rules = [
        check_product_name(fields),
        check_mrp(fields),
        check_net_quantity(fields),
        check_manufacturer(fields),
        check_date_information(fields),
        check_consumer_care(fields),
        check_country_of_origin(fields),
    ]

    pass_count = sum(
        1
        for rule in rules
        if rule["status"] == "PASS"
    )

    fail_count = sum(
        1
        for rule in rules
        if rule["status"] == "FAIL"
    )

    not_verifiable_count = sum(
        1
        for rule in rules
        if rule["status"] == "NOT_VERIFIABLE"
    )

    total_weight = sum(
        rule["weight"]
        for rule in rules
    )

    earned_weight = sum(
        rule["weight"]
        for rule in rules
        if rule["status"] == "PASS"
    )

    if total_weight > 0:
        compliance_score = round(
            (
                earned_weight
                / total_weight
            )
            * 100,
            2,
        )
    else:
        compliance_score = 0.0

    if fail_count > 0:
        overall_status = (
            "POTENTIAL_VIOLATION"
        )
    elif not_verifiable_count > 0:
        overall_status = (
            "NEEDS_REVIEW"
        )
    else:
        overall_status = (
            "COMPLIANT"
        )

    if compliance_score > 75:
        score_level = "GREEN"
    elif compliance_score >= 50:
        score_level = "YELLOW"
    else:
        score_level = "RED"

    return {
        "overall_status": overall_status,
        "compliance_score": compliance_score,
        "score_level": score_level,
        "summary": {
            "total_rules": len(rules),
            "total_weight": total_weight,
            "earned_weight": earned_weight,
            "passed": pass_count,
            "failed": fail_count,
            "not_verifiable": not_verifiable_count,
        },
        "rules": rules,
        "disclaimer": (
            "This result is an AI-assisted "
            "compliance screening and does not "
            "constitute a final legal determination."
        ),
    }


def run_rule_engine(
    fields: dict[str, Any],
) -> dict[str, Any]:
    return evaluate_compliance(
        fields
    )