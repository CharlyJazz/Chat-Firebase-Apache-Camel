package com.service.bus.apachecamelservicebus.routes;

import org.apache.camel.AggregationStrategy;
import org.apache.camel.Exchange;

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
        	messagesByUser = new MessagesByUser(message.getFrom_user(), message.getBody());
            newExchange.getIn().setBody(messagesByUser);
            return newExchange;
        } else {
        	MessagesByUser currentMessagesByUser = oldExchange.getIn().getBody(MessagesByUser.class);
        	currentMessagesByUser.addMessage(message.getBody());
        	return oldExchange;
        }			
	}

}