def add_resource_change(report: dict, resource_name: str, amount: int | float) -> None:
    report["resource_changes"][resource_name] = (
        report["resource_changes"].get(resource_name, 0) + amount
    )


def add_stat_change(report: dict, stat_name: str, amount: int | float) -> None:
    report["stat_changes"][stat_name] = (
        report["stat_changes"].get(stat_name, 0) + amount
    )