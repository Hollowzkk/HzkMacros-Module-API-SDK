package com.example.firstmodule;

import dev.hzk.hzkmacros.api.module.HzkModule;
import dev.hzk.hzkmacros.api.module.ModuleContext;
import dev.hzk.hzkmacros.api.module.ModuleResult;
import dev.hzk.hzkmacros.api.module.ModuleValue;

public final class FirstModule implements HzkModule {
    @Override
    public void onLoad(ModuleContext context) {
        context.logger().info("First Module loaded!");

        context.registerVariable(
            "&first_module_status",
            () -> ModuleValue.string("ready")
        );

        context.registerAction("HELLO", invocation -> {
            String name = invocation.argument(0, "player");
            invocation.log("Hello, " + name + "!");
            return ModuleResult.done();
        });
    }
}
