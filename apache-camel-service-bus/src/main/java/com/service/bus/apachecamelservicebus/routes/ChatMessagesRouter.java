package com.service.bus.apachecamelservicebus.routes;

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.model.dataformat.JsonLibrary;
import org.springframework.stereotype.Component;

@Component
public class ChatMessagesRouter extends RouteBuilder {
	@Override
	public void configure() throws Exception {
		from("kafka:chat_messages")
		.unmarshal().json(JsonLibrary.Jackson, ChatMessage.class) 
		.aggregate(simple("${body.from_user}"), new MesssagesAggregationStrategy())
		.completionSize(3)
		.completionTimeout(1500)
		.log("${body.user_id} Mesage list -> ${body.list_of_messages}")
		.to("log:chat-message-received -> End of Pipeline");
	}
}