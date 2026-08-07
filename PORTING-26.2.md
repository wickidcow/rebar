# Rebar 26.2 port

This source tree targets **Minecraft/Paper 26.2** and **Java 25**. The recommended fork release tag is **`0.42.1-26.2`**, preserving the current upstream Rebar `0.42.1` release line while making the Minecraft target explicit.

## Compatibility goals

- Preserve the existing Rebar public addon API wherever Minecraft 26.2 does not force an API break.
- Recompile the NMS module against the Paper 26.2 development bundle.
- Use Bukkit's Minecraft version directly for the startup compatibility check instead of parsing Paper implementation/build strings.
- Keep packet translation fail-open so an internal translation failure cannot suppress a vanilla inventory, recipe, or merchant packet.
- Never mutate the live `MerchantOffer`/`ItemCost` data when translating merchant packets for the client.
- Preserve the original server-side `ItemCost` matching predicate while translating only a copied display stack.
- Avoid initializing metrics or coroutine infrastructure from `onDisable()` after an early startup failure.
- Ensure changes under `nms/**` trigger CI and live tests.
- Keep GUI support on **InvUI 2.2.0**, which is the InvUI line updated for Minecraft 26.2. This also picks up the packet-listener initialization fix introduced after 2.1.0.
- Align Rebar test dependencies with **Adventure 5.2.0** for the Minecraft 26.2/Paper 26.2 ecosystem. The source scan found no removed Adventure 4 APIs that require Rebar source changes.

## Build and test

Run with JDK 25:

```bash
python3 scripts/verify_26_2_port.py
./gradlew :rebar:shadowJar -Pversion=0.42.1-26.2
./gradlew :test:runServer -Pversion=0.42.1-26.2
```

To make the matching API available to a local Pylon build:

```bash
./gradlew :rebar:publishToMavenLocal -Pversion=0.42.1-26.2
```

## Required validation before release

On a clean Paper 26.2 test server verify:

- `/rebar` and `/rebar menu` open and render all item icons.
- Vanilla villagers show both input and result items and trades complete normally.
- Rebar-localized items render in normal inventories, equipment, bundles/containers, and merchant trades.
- Recipe book, ghost recipes, shaped/shapeless crafting, furnaces, smithing, and stonecutting work.
- Block texture entities/culling still render and update.
- Rebar storage survives chunk unload/reload and a complete server restart.
- Disabling after an intentionally failed startup does not initialize metrics or schedule tasks while disabled.

The version bypass should **not** be enabled for a build produced from this tree. The generated plugin metadata and the explicit runtime version check both target 26.2.

See `NMS-26.2-AUDIT.md` for the Minecraft-internal surface that must be re-audited on the next Minecraft update.
