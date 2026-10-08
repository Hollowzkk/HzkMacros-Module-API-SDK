package com.example.advanced;

import dev.hzk.hzkmacros.api.module.HzkModule;
import dev.hzk.hzkmacros.api.module.ModuleContext;
import dev.hzk.hzkmacros.api.module.ModuleEvent;
import dev.hzk.hzkmacros.api.module.ModuleLogger;
import dev.hzk.hzkmacros.api.module.ModuleResult;
import dev.hzk.hzkmacros.api.module.ModuleTask;
import dev.hzk.hzkmacros.api.module.ModuleValue;
import java.util.List;
import java.util.Map;

public final class AdvancedModule implements HzkModule {
    private ModuleLogger logger;
    private ModuleTask heartbeat;

    @Override
    public void onLoad(ModuleContext context) {
        this.logger = context.logger();
        ModuleEvent ping = context.registerEvent("advanced_ping");

        context.registerVariable("&advanced_status", () -> ModuleValue.string("ready"));
        context.registerIterator("advanced_samples", () -> List.of(
            Map.of("NAME", ModuleValue.string("first"), "NUMBER", ModuleValue.integer(1)),
            Map.of("NAME", ModuleValue.string("second"), "NUMBER", ModuleValue.integer(2))
        ));

        context.registerAction("ADVANCEDPING", invocation -> {
            String message = invocation.argument(0, "ping");
            invocation.log("Advanced: " + message);
            ping.emit(Map.of("MESSAGE", ModuleValue.string(message)));
            return ModuleResult.done();
        });

        this.heartbeat = context.scheduler().repeat(20, 20 * 60, () ->
            logger.info("heartbeat tick=" + context.scheduler().currentTick()));

        logger.info("Data directory: " + context.dataDirectory());
    }

    @Override
    public void onUnload() {
        if (heartbeat != null) heartbeat.cancel();
        if (logger != null) logger.info("Advanced Module unloaded");
    }
}
