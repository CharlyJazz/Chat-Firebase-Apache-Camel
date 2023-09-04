package com.service.bus.apachecamelservicebus.routes;

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.component.kafka.KafkaConstants;
import org.apache.camel.model.dataformat.JsonLibrary;
import org.springframework.stereotype.Component;

@Component
public class ChatMessagesRouter extends RouteBuilder {
	@Override
	public void configure() throws Exception {
		from("kafka:chat_messages")
		.unmarshal().json(JsonLibrary.Jackson, ChatMessage.class) 
		.aggregate(simple("${body.from_user}-${body.chat_id}"), new MesssagesAggregationStrategy())
		.completionSize(10)
		.completionTimeout(3000)
		.log("${body.from_user} Mesage list -> ${body.list_of_messages}")
		.setHeader(KafkaConstants.KEY, simple("${body.chat_id}"))
		.marshal().json(JsonLibrary.Jackson) 
		.setBody(simple("${body}"))
		.to("kafka:chat_messages_grouped");
	}
}