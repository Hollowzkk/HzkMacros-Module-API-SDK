package com.example.consumer;

import com.example.provider.api.GreetingService;
import dev.hzk.hzkmacros.api.module.HzkModule;
import dev.hzk.hzkmacros.api.module.ModuleContext;
import dev.hzk.hzkmacros.api.module.ModuleResult;

public final class HelloConsumerModule implements HzkModule {
    @Override
    public void onLoad(ModuleContext context) {
        var provider = context.findModule("hello_provider").orElseThrow();
        context.logger().info("Using " + provider.name() + " " + provider.version());

        GreetingService greetings = context.services().require(
            "hello_provider", "greeting", GreetingService.class
        );

        context.messages().subscribe("hello_provider:used", message ->
            context.logger().info("Provider message: " + message.values()));

        context.registerAction("CONSUMERHELLO", invocation -> {
            invocation.log(greetings.greet(invocation.argument(0, "consumer")));
            return ModuleResult.done();
        });
    }
}
