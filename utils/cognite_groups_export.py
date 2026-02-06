from __future__ import annotations

from pathlib import Path
from typing import Iterable
import re

import pandas as pd

from cognite_auth import CUSTOMER_CONFIGS, interactive_client


def extract_resource_name(capability) -> str:
    """Extract resource name from capability type (e.g., TimeSeriesAcl -> timeseries)."""
    type_name = type(capability).__name__
    if type_name.endswith("Acl"):
        resource = type_name[:-3]
    else:
        resource = type_name
    return re.sub(r"(?<!^)(?=[A-Z])", "_", resource).lower()


def extract_action_name(action) -> str:
    """Extract action name from action object (e.g., Action.Read -> read)."""
    if hasattr(action, "name"):
        return str(action.name).lower()
    if hasattr(action, "value"):
        return str(action.value).lower()

    action_str = str(action)
    if "Action." in action_str:
        parts = action_str.split("Action.")[-1]
        action_name = parts.split(":")[0].split("'")[0].split(">")[0].strip()
    elif "." in action_str:
        action_name = action_str.split(".")[-1].split(":")[0].split("'")[0].split(">")[0].strip()
    else:
        action_name = action_str.split(":")[0].split("'")[0].split(">")[0].strip()

    return action_name.lower()


def is_all_scope(scope) -> bool:
    """Check if scope is AllScope."""
    if scope is None:
        return True
    scope_type = type(scope).__name__
    if scope_type == "AllScope":
        return True
    if hasattr(scope, "all"):
        return True
    return False


def extract_scope_string(scope) -> str | None:
    """Extract scope string from capability scope object. Returns None for AllScope."""
    if is_all_scope(scope):
        return None

    scope_parts = []
    for attr in ["data_set_id", "data_set_ids", "project", "project_id", "project_ids"]:
        if hasattr(scope, attr):
            value = getattr(scope, attr)
            if value:
                if isinstance(value, (list, tuple)):
                    scope_parts.append(f"{attr}={','.join(str(v) for v in value)}")
                else:
                    scope_parts.append(f"{attr}={value}")

    if not scope_parts:
        scope_str = str(scope)
        if scope_str.startswith("Scope(") and scope_str.endswith(")"):
            scope_str = scope_str[6:-1]
        scope_parts.append(scope_str)

    return ":".join(scope_parts) if scope_parts else None


def extract_capability_key(capability) -> str | list[str] | None:
    """Extract standardized capability key(s) in format: resource:action or resource:action:scope."""
    if not hasattr(capability, "actions") or not capability.actions:
        return None

    resource = extract_resource_name(capability)

    action_names = []
    for action in capability.actions:
        action_name = extract_action_name(action)
        if action_name:
            action_names.append(action_name)

    if not action_names:
        return None

    action_names = sorted(set(action_names))

    capability_keys = []
    for action in action_names:
        cap_key = f"{resource}:{action}"
        if hasattr(capability, "scope") and capability.scope:
            scope_str = extract_scope_string(capability.scope)
            if scope_str:
                cap_key = f"{cap_key}:{scope_str}"
        capability_keys.append(cap_key)

    return capability_keys if len(capability_keys) > 1 else capability_keys[0]


def collect_all_capabilities(groups_by_customer: dict) -> list[str]:
    """Collect all unique capabilities across all customers."""
    all_capabilities = set()

    for groups in groups_by_customer.values():
        if groups is None:
            continue

        for group in groups:
            if hasattr(group, "capabilities") and group.capabilities:
                for cap in group.capabilities:
                    cap_keys = extract_capability_key(cap)
                    if cap_keys:
                        if isinstance(cap_keys, list):
                            for key in cap_keys:
                                all_capabilities.add(key)
                        else:
                            all_capabilities.add(cap_keys)

    return sorted(list(all_capabilities))


def parse_capability_key(cap_key: str) -> tuple[str, str, str | None]:
    """Parse a capability key into (resource, action, scope)."""
    parts = cap_key.split(":")
    resource = parts[0]
    action = parts[1] if len(parts) > 1 else ""
    scope = ":".join(parts[2:]) if len(parts) > 2 else None
    return (resource, action, scope)


def build_group_row(group, all_resources: set[str]) -> dict:
    """Build a single row dictionary for a group with resource-based capabilities."""
    row = {
        "Group Name": getattr(group, "name", ""),
        "Group ID": getattr(group, "id", ""),
        "Source ID": getattr(group, "source_id", ""),
    }

    resource_actions = {resource: set() for resource in all_resources}

    if hasattr(group, "capabilities") and group.capabilities:
        for cap_obj in group.capabilities:
            cap_keys = extract_capability_key(cap_obj)
            if cap_keys:
                keys_list = cap_keys if isinstance(cap_keys, list) else [cap_keys]

                for key in keys_list:
                    resource, action, scope = parse_capability_key(key)
                    if resource in resource_actions:
                        if scope:
                            resource_actions[resource].add(f"{action}:{scope}")
                        else:
                            resource_actions[resource].add(action)

    for resource in all_resources:
        actions_list = sorted(resource_actions[resource])
        row[resource] = ", ".join(actions_list) if actions_list else "n/a"

    return row


def collect_all_resources(groups_by_customer: dict) -> set[str]:
    """Collect all unique resources across all customers."""
    all_resources = set()

    for groups in groups_by_customer.values():
        if groups is None:
            continue

        for group in groups:
            if hasattr(group, "capabilities") and group.capabilities:
                for cap in group.capabilities:
                    cap_keys = extract_capability_key(cap)
                    if cap_keys:
                        keys_list = cap_keys if isinstance(cap_keys, list) else [cap_keys]
                        for key in keys_list:
                            resource, _, _ = parse_capability_key(key)
                            all_resources.add(resource)

    return all_resources


def build_customer_dataframe(groups, all_resources: set[str]) -> pd.DataFrame:
    """Build a DataFrame for a customer's groups with resource-based capability columns."""
    rows = [build_group_row(group, all_resources) for group in groups]
    df = pd.DataFrame(rows)

    group_cols = ["Group Name", "Group ID", "Source ID"]
    resource_cols = sorted([r for r in all_resources if r in df.columns])

    resource_cols_with_data = []
    for col in resource_cols:
        if col in df.columns:
            if (df[col] != "n/a").any():
                resource_cols_with_data.append(col)

    return df[group_cols + resource_cols_with_data]


def write_groups_to_excel(
    dataframes_by_customer: dict[str, pd.DataFrame | None],
    output_file: Path | str,
) -> None:
    """Write groups data to Excel with one sheet per customer."""
    output_path = Path(output_file)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for customer_name, df in dataframes_by_customer.items():
            sheet_name = customer_name[:31]

            if df is None:
                pd.DataFrame({"Error": ["Failed to fetch groups"]}).to_excel(
                    writer, sheet_name=sheet_name, index=False
                )
                continue

            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"✓ Saved {len(df)} groups for {customer_name} to sheet '{sheet_name}'")

    print(f"\n✅ Excel file saved: {output_path.absolute()}")


def print_user_profile(client, token_cache_path: Path) -> None:
    """Fetch and print the logged-in user's profile."""
    user_profile = client.iam.user_profiles.me()
    print(f"User Identifier: {user_profile.user_identifier}")
    print(f"Name: {user_profile.given_name} {user_profile.surname}")
    print(f"Email: {user_profile.email}")
    print(f"Full profile: {user_profile}")
    print(token_cache_path)


def print_raw_capabilities(groups_by_customer: dict, max_groups_preview: int = 3) -> None:
    """Display raw capabilities for a small preview of groups per customer."""
    print("=" * 80)
    print("RAW CAPABILITIES FROM GROUPS")
    print("=" * 80)

    for customer_name, groups in groups_by_customer.items():
        if groups is None:
            print(f"\n{customer_name}: No groups (error occurred)")
            continue

        print(f"\n{'=' * 80}")
        print(f"Customer: {customer_name} ({len(groups)} groups)")
        print(f"{'=' * 80}")

        for i, group in enumerate(groups[:max_groups_preview], 1):
            print(f"\n--- Group {i}: {getattr(group, 'name', 'Unknown')} ---")
            print(f"Group ID: {getattr(group, 'id', 'N/A')}")
            print(f"Source ID: {getattr(group, 'source_id', 'N/A')}")

            if hasattr(group, "capabilities") and group.capabilities:
                print(f"\nCapabilities ({len(group.capabilities)} total):")
                for j, cap in enumerate(group.capabilities, 1):
                    print(f"\n  Capability {j}:")
                    print(f"    Type: {type(cap).__name__}")
                    print(f"    Raw object: {cap}")
                    print(f"    Attributes: {dir(cap)}")

                    for attr in dir(cap):
                        if not attr.startswith("_"):
                            try:
                                value = getattr(cap, attr)
                                if not callable(value):
                                    print(f"      {attr}: {value}")
                            except Exception:
                                pass
            else:
                print("\nNo capabilities")

        if len(groups) > max_groups_preview:
            print(f"\n... and {len(groups) - max_groups_preview} more groups (showing first {max_groups_preview} only)")


def export_groups(
    customers: Iterable[str] | None = None,
    output_file: Path | str = "groups_by_customer.xlsx",
    token_cache_dir: Path | None = None,
    profile_customer: str | None = None,
    show_profile: bool = True,
    show_raw_capabilities: bool = False,
    max_groups_preview: int = 3,
    verbose: bool = True,
) -> tuple[dict[str, pd.DataFrame | None], Path]:
    """Fetch groups for customers, build DataFrames, and export to Excel."""
    customer_list = list(customers) if customers is not None else list(CUSTOMER_CONFIGS.keys())
    if not customer_list:
        raise ValueError("No customers specified.")

    token_cache_dir = token_cache_dir or (Path.home() / ".cognite" / "token_cache")
    output_path = Path(output_file)
    profile_customer = profile_customer or customer_list[0]

    groups_by_customer: dict[str, object | None] = {}
    dataframes_by_customer: dict[str, pd.DataFrame | None] = {}

    for customer_name in customer_list:
        if verbose:
            print(f"Fetching groups for customer: {customer_name}")
        try:
            cache_path = token_cache_dir / f"{customer_name}.json" if token_cache_dir else None
            customer_client = interactive_client(customer_name, cache_path)

            if show_profile and customer_name == profile_customer and cache_path is not None:
                print_user_profile(customer_client, cache_path)

            groups = customer_client.iam.groups.list(all=True)
            groups_by_customer[customer_name] = groups

            if verbose:
                print(f"  ✓ Found {len(groups)} groups for {customer_name}")
        except Exception as exc:
            if verbose:
                print(f"  ✗ Error fetching groups for {customer_name}: {exc}")
            groups_by_customer[customer_name] = None
            dataframes_by_customer[customer_name] = None

    if verbose:
        print(f"\nTotal customers processed: {len(customer_list)}")

    if show_raw_capabilities:
        print_raw_capabilities(groups_by_customer, max_groups_preview=max_groups_preview)

    all_resources = collect_all_resources(groups_by_customer)

    for customer_name, groups in groups_by_customer.items():
        if groups is None:
            dataframes_by_customer[customer_name] = None
        else:
            dataframes_by_customer[customer_name] = build_customer_dataframe(groups, all_resources)

    write_groups_to_excel(dataframes_by_customer, output_path)
    return dataframes_by_customer, output_path
