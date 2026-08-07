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
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/packet/PlayerPacketHandler.kt", "DataComponentExactPredicate.allOf")
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/packet/PlayerPacketHandler.kt", "PatchedDataComponentMap.fromPatch(DataComponentMap.EMPTY, costStack.componentsPatch)")
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/packet/PlayerPacketHandler.kt", "ItemCost(costStack.typeHolder(), costStack.count, costPredicate, costStack)")
forbid("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/packet/PlayerPacketHandler.kt", "ItemCost(itemCost.item, itemCost.count, itemCost.components, costStack)")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/datatypes/KeyedPersistentDataType.kt", "import java.util.function.Function")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/datatypes/KeyedPersistentDataType.kt", "retrievalFunction: Function<NamespacedKey, T>")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/datatypes/KeyedPersistentDataType.kt", "retrievalFunction.apply(key)")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/datatypes/KeyedPersistentDataType.kt", "@JvmSynthetic")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/Rebar.kt", "Bukkit.getMinecraftVersion()")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/Rebar.kt", "minecraftVersionsMatch(actualVersion, expectedVersion)")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/Rebar.kt", "checkNotNull(pluginMeta.apiVersion)")
forbid("rebar/src/main/kotlin/io/github/pylonmc/rebar/Rebar.kt", "val expectedVersion = pluginMeta.apiVersion\n")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/Rebar.kt", "normalizeMinecraftVersion")
forbid("rebar/src/main/kotlin/io/github/pylonmc/rebar/Rebar.kt", "if (actualVersion != expectedVersion)")
require("rebar/src/main/kotlin/io/github/pylonmc/rebar/Rebar.kt", "if (metricsInitialized)")
require(".github/workflows/gradle.yml", "- 'nms/**'")
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/NmsAccessorImpl.kt", "Vec3.atCenterOf(nmsPos)")
forbid("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/NmsAccessorImpl.kt", "nmsPos.center")
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/entity/BlockTextureEntityImpl.kt", "nextEntityId(block.block.world)")
forbid("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/entity/BlockTextureEntityImpl.kt", "nextEntityId()")
require("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/entity/BlockTextureEntityImpl.kt", "EntityTypes.ITEM_DISPLAY")
forbid("nms/src/main/kotlin/io/github/pylonmc/rebar/nms/entity/BlockTextureEntityImpl.kt", "EntityType.ITEM_DISPLAY")

if errors:
    print("Rebar 26.2 port verification failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("Rebar 26.2 port static verification passed.")
