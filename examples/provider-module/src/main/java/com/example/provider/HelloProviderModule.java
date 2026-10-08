package com.example.provider;

import com.example.provider.api.GreetingService;
import dev.hzk.hzkmacros.api.module.HzkModule;
import dev.hzk.hzkmacros.api.module.ModuleContext;
import dev.hzk.hzkmacros.api.module.ModuleResult;
import dev.hzk.hzkmacros.api.module.ModuleValue;
import java.util.Map;

public final class HelloProviderModule implements HzkModule {
    @Override
    public void onLoad(ModuleContext context) {
        GreetingService greetings = name -> "Hello, " + (name == null || name.isBlank() ? "player" : name) + "!";
        context.services().register("greeting", greetings);

        context.registerAction("PROVIDERHELLO", invocation -> {
            String message = greetings.greet(invocation.argument(0, "player"));
            invocation.log(message);
            context.messages().publish("used", Map.of("MESSAGE", ModuleValue.string(message)));
            return ModuleResult.done();
        });
    }
}
