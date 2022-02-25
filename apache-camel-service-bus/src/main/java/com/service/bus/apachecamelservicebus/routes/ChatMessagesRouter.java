package com.service.bus.apachecamelservicebus.routes;

import org.apache.camel.builder.RouteBuilder;
import org.springframework.stereotype.Component;

@Component
public class ChatMessagesRouter extends RouteBuilder {
	@Override
	public void configure() throws Exception {
		from("kafka:chat")
		.log("${body}")
		.to("log:chat-message-received {body}");
	}
}
