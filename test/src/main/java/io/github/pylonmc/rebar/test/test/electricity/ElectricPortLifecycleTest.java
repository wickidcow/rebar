package io.github.pylonmc.rebar.test.test.electricity;

import io.github.pylonmc.rebar.electricity.ElectricityManager;
import io.github.pylonmc.rebar.electricity.nodes.ElectricConsumerNode;
import io.github.pylonmc.rebar.electricity.nodes.ElectricPortEntity;
import io.github.pylonmc.rebar.electricity.nodes.ElectricPortSpec;
import io.github.pylonmc.rebar.event.RebarElectricNodeRemoveEvent;
import io.github.pylonmc.rebar.test.RebarTest;
import io.github.pylonmc.rebar.test.base.SyncTest;
import io.github.pylonmc.rebar.util.position.BlockPosition;
import org.bukkit.block.Block;
import org.bukkit.block.BlockFace;

import java.util.Arrays;

import static org.assertj.core.api.Assertions.assertThat;

/** Regression: an unloaded/orphaned electric port must not break unrelated node removals. */
public class ElectricPortLifecycleTest extends SyncTest {

    @Override
    protected void test() {
        Block block = RebarTest.testWorld.getSpawnLocation().getBlock();
        BlockPosition position = new BlockPosition(block);

        // The port entity exists, but its block node is not in ElectricityManager.
        ElectricConsumerNode orphanNode = new ElectricConsumerNode("orphan", position, 0.0);
        ElectricPortEntity port = new ElectricPortEntity(block, new ElectricPortSpec(orphanNode, BlockFace.NORTH));

        try {
            assertThat(isListening(port)).isTrue();

            // Previously the port's listener dereferenced the missing node and threw.
            ElectricConsumerNode unrelatedNode = new ElectricConsumerNode("unrelated", position, 0.0);
            ElectricityManager.addNode(unrelatedNode);
            try {
                ElectricityManager.removeNode(unrelatedNode);
            } finally {
                if (ElectricityManager.getNodeById(unrelatedNode.getId()) != null) {
                    ElectricityManager.removeNode(unrelatedNode);
                }
            }

            assertThat(isListening(port)).isTrue();

            // EntityStorage calls this on chunk unload: it must release Bukkit listeners.
            port.onUnload();
            assertThat(isListening(port)).isFalse();
        } finally {
            port.remove();
        }
    }

    private static boolean isListening(ElectricPortEntity port) {
        return Arrays.stream(RebarElectricNodeRemoveEvent.getHandlerList().getRegisteredListeners())
                .anyMatch(listener -> listener.getListener() == port);
    }
}
