def add_resource_change(report: dict, resource_name: str, amount: int | float) -> None:
    report["resource_changes"][resource_name] = (
        report["resource_changes"].get(resource_name, 0) + amount
    )


def add_stat_change(report: dict, stat_name: str, amount: int | float) -> None:
    report["stat_changes"][stat_name] = (
        report["stat_changes"].get(stat_name, 0) + amount
    )

    
def merge_reports(target: dict, source: dict) -> None:
    for resource, change in source.get("resource_changes", {}).items():
        target["resource_changes"][resource] = (
            target["resource_changes"].get(resource, 0) + change
        )

    for stat, change in source.get("stat_changes", {}).items():
        target["stat_changes"][stat] = (
            target["stat_changes"].get(stat, 0) + change
        )

    target["messages"].extend(source.get("messages", []))