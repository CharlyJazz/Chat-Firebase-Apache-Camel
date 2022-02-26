package com.service.bus.apachecamelservicebus.routes;

import org.apache.camel.AggregationStrategy;
import org.apache.camel.Exchange;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.model.dataformat.JsonLibrary;
import org.springframework.stereotype.Component;

@Component
public class ChatMessagesRouter extends RouteBuilder {
	/**
	* https://camel.apache.org/components/next/eips/aggregate-eip.html#_aggregate_options
	* This is amazing. The collection expression should be user_id
	* If the oldExchange is null that mean is not a MessagesByUser instance
	* then send newExchange as a MessagesByUser instance with the user_id and the first message
	* If oldExchange is not null then just add message to it.
	* We do not need specify if the newExchange user id is the same of the oldExchange
	* This is made by the collection expression parameter "user_id" 
	* This is MAGIC.
	*/
	public class MesssagesAggregationStrategy implements AggregationStrategy {

		@Override
		public Exchange aggregate(Exchange oldExchange, Exchange newExchange) {			
			ChatMessage message = newExchange.getIn().getBody(ChatMessage.class);

			MessagesByUser messagesByUser = null;

	        if (oldExchange == null) {
	        	messagesByUser = new MessagesByUser(message.getUser_id(), message.getMessage());
	            newExchange.getIn().setBody(messagesByUser);
	            return newExchange;
	        } else {
	        	MessagesByUser currentMessagesByUser = oldExchange.getIn().getBody(MessagesByUser.class);
	        	currentMessagesByUser.addMessage(message.getMessage());
	        	return oldExchange;
	        }			
		}

	}

	@Override
	public void configure() throws Exception {
		from("kafka:chat")
		.unmarshal().json(JsonLibrary.Jackson, ChatMessage.class) 
		.aggregate(simple("${body.user_id}"), new MesssagesAggregationStrategy())
		.completionSize(3)
		.completionTimeout(1500)
		.log("${body.user_id} Mesage list -> ${body.list_of_messages}")
		.to("log:chat-message-received -> End of Pipeline");
	}
}
