# Rebar NMS audit — Minecraft 26.2

This document records the Minecraft-internal surface used by Rebar's `nms` module for the **26.2** port. It is intentionally kept separate from the public Rebar API so a future Minecraft update can be audited primarily inside `nms/**`.

## Packet and merchant surface

The 26.2 port was checked against the current 26.2 mappings/API surface for:

- `ClientboundMerchantOffersPacket`
  - merchant container id
  - offers
  - villager level/xp
  - progress/restock flags
- `MerchantOffer`
  - input costs
  - result stack
  - uses/max uses
  - experience
  - price multiplier/demand
  - special price/reward-exp/ignore-discounts state
- `ItemCost`
  - item holder
  - count
  - `DataComponentExactPredicate`
  - display `ItemStack`
- `ClientboundContainerSetContentPacket`
- `ClientboundContainerSetSlotPacket`
- `ClientboundSetCursorItemPacket`
- `ServerboundContainerClickPacket`
- `ClientboundRecipeBookAddPacket`
- `RecipeDisplayEntry`

### Merchant translation invariant

The translated merchant packet must not rewrite the server-side ingredient predicate. Rebar now translates a **copy** of `ItemCost.itemStack` for display and reconstructs the cost with the original:

- item holder
- count
- component predicate

This prevents localization/client presentation data from becoming part of the actual villager trade-matching rules and prevents translation from mutating the live offer stack.

## Recipe/crafting reflection surface

The following internal/private members are deliberately accessed by the 26.2 NMS implementation and must be re-checked whenever the Minecraft target changes:

| Owner | Member/surface |
| --- | --- |
| `StackedItemContents` | `raw` |
| `ServerPlaceRecipe` | constructor |
| `ServerPlaceRecipe` | `clearGrid` |
| `ServerPlaceRecipe` | `placeRecipe` |
| `ServerPlaceRecipe` | `testClearGrid` |
| `AbstractCraftingMenu` | `beginPlacingRecipe` |
| `AbstractCraftingMenu` | `finishPlacingRecipe` |
| `AbstractFurnaceBlockEntity` | `quickCheck` |

## Entity/registry reflection surface

| Owner | Member/surface |
| --- | --- |
| `SynchedEntityData` | `ID_REGISTRY` |
| `SynchedEntityData.Builder` | `itemsById` |
| `LootContextParamSets` | `REGISTRY` |

## Failure containment

Packet translation is deliberately fail-open. Rebar catches ordinary exceptions and linkage errors around translation, logs a diagnostic once per direction/packet class, and forwards the original vanilla packet. A compatibility defect should therefore degrade Rebar-specific presentation rather than silently deleting a vanilla inventory/merchant/recipe packet.

Fatal VM errors are not swallowed.

## 26.2 GUI/dependency boundary

Rebar's GUI stack is pinned to **InvUI 2.2.0** for this port. Rebar's explicit Adventure test dependencies are pinned to **Adventure 5.2.0** so tests exercise the same major Adventure generation used by the 26.2 ecosystem.

## Checklist for a future Minecraft target

Before changing `minecraft.version` again:

1. Recompile the complete `nms` module against the new Paper development bundle.
2. Re-check every field/method in the reflection tables above.
3. Re-check all merchant, inventory, click, recipe-book, bundle, equipment, and entity-metadata packet constructors/accessors.
4. Confirm the current InvUI release explicitly supports the new Minecraft version.
5. Run `scripts/verify_26_2_port.py` (or rename/update it for the new target).
6. Run the Rebar live test server workflow.
7. Manually test `/rebar menu`, vanilla villager trading, recipe-book placement, furnaces/smithing, custom block rendering, and restart persistence.
8. Only then update the Pylon Rebar dependency to the new Rebar implementation/API artifact.
