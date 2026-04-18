import json
from pathlib import Path
import re

def parse_ipconfig(ipconfig_text: str) -> list:
    adapters = []
    current_adapter = None
    current_property = None
    lines = ipconfig_text.strip().split("\n")
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if not line.startswith(" ") and not line.startswith("\t") and line_stripped.endswith(":"):
            adapter_name = line_stripped[:-1].strip()
            current_adapter = {
                "adapter_name": adapter_name,
                "description": "",
                "physical_address": "",
                "dhcp_enabled": "",
                "ipv4_address": "",
                "subnet_mask": "",
                "default_gateway": "",
                "dns_servers": []
            }
            adapters.append(current_adapter)
            current_property = None
            continue
        if current_adapter is None:
            continue
        if line.startswith(" ") or line.startswith("\t"):
            if ":" in line_stripped:
                parts = line_stripped.split(":", 1)
                key = parts[0].replace(".", "").strip().lower()
                val = re.sub(r"\(.*\)", "", parts[1].strip()).strip()
                if key == "description":
                    current_adapter["description"] = val
                    current_property = "description"
                elif key == "physical address":
                    current_adapter["physical_address"] = val
                    current_property = "physical_address"
                elif key == "dhcp enabled":
                    current_adapter["dhcp_enabled"] = val
                    current_property = "dhcp_enabled"
                elif key in ["ipv4 address", "autoconfiguration ipv4 address"]:
                    current_adapter["ipv4_address"] = val
                    current_property = "ipv4_address"
                elif key == "subnet mask":
                    current_adapter["subnet_mask"] = val
                    current_property = "subnet_mask"
                elif key == "default gateway":
                    current_adapter["default_gateway"] = val
                    current_property = "default_gateway"
                elif key == "dns servers":
                    if val:
                        current_adapter["dns_servers"].append(val)
                    current_property = "dns_servers"
                else:
                    current_property = None
            else:
                val = re.sub(r"\((Preferred|Deferred)\)", "", line_stripped).strip()
                if val and current_property:
                    if current_property == "dns_servers":
                        current_adapter["dns_servers"].append(val)
                    elif current_property == "default_gateway":
                        if current_adapter["default_gateway"]:
                            current_adapter["default_gateway"] += f", {val}"
                        else:
                            current_adapter["default_gateway"] = val
    return adapters

def main():
    result = [{"file_name": path.name, "adapters": parse_ipconfig(path.read_text(encoding="utf-16-le"))} for path in sorted(Path(".").glob("*.txt"))]
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
