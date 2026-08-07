#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def require(path: str, needle: str) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    if needle not in text:
        errors.append(f"{path}: missing {needle!r}")

def forbid(path: str, needle: str) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    if needle in text:
        errors.append(f"{path}: still contains {needle!r}")

require("gradle.properties", "minecraft.version=26.2")
require("rebar/build.gradle.kts", "xyz.xenondevs.invui:invui:2.2.0")
require("rebar/build.gradle.kts", "xyz.xenondevs.invui:invui-kotlin:2.2.0")
forbid("rebar/build.gradle.kts", "xyz.xenondevs.invui:invui:2.1.0")
forbid("rebar/build.gradle.kts", "xyz.xenondevs.invui:invui-kotlin:2.1.0")
require("rebar/build.gradle.kts", "net.kyori:adventure-api:5.2.0")
require("rebar/build.gradle.kts", "net.kyori:adventure-text-minimessage:5.2.0")
forbid("rebar/build.gradle.kts", "net.kyori:adventure-api:4.20.0")
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/packet/PlayerPacketHandler.kt", "catch (e: LinkageError)")
forbid("gradle.properties", "minecraft.version=26.1.2")
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/packet/PlayerPacketHandler.kt", "handleOutgoingPacketSafely")
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/packet/PlayerPacketHandler.kt", "itemCost.itemStack.copy()")
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/packet/PlayerPacketHandler.kt", "ItemCost(itemCost.item, itemCost.count, itemCost.components, costStack)")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/Rebar.kt", "Bukkit.getMinecraftVersion()")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/Rebar.kt", "if (metricsInitialized)")
require(".github/workflows/gradle.yml", "- 'nms/**'")

if errors:
    print("Rebar 26.2 port verification failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("Rebar 26.2 port static verification passed.")
