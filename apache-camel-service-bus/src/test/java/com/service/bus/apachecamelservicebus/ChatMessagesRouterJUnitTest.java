package com.service.bus.apachecamelservicebus;

import org.apache.camel.RoutesBuilder;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.component.mock.MockEndpoint;
import org.apache.camel.model.dataformat.JsonLibrary;
import org.apache.camel.test.junit5.CamelTestSupport;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.service.bus.apachecamelservicebus.routes.ChatMessage;
import com.service.bus.apachecamelservicebus.routes.MessagesByUser;
import com.service.bus.apachecamelservicebus.routes.MesssagesAggregationStrategy;

public class ChatMessagesRouterJUnitTest extends CamelTestSupport {
    private static final Logger LOG = LoggerFactory.getLogger(CamelTestSupport.class);

    @Test
    public void testMock() throws Exception {

        template.sendBody("direct:chat_messages", "{\"from_user\": 1, \"to_user\": 2, \"body\": \"Hell 1\", \"chat_id\": 1}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 1, \"to_user\": 2, \"body\": \"Hell 2\", \"chat_id\": 1}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 1, \"to_user\": 2, \"body\": \"Hell 3\", \"chat_id\": 1}");

        template.sendBody("direct:chat_messages", "{\"from_user\": 2, \"to_user\": 2, \"body\": \"Hell 1\", \"chat_id\": 1}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 2, \"to_user\": 2, \"body\": \"Hell 2\", \"chat_id\": 1}");
        
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 1\", \"chat_id\": 1}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 2\", \"chat_id\": 1}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 3\", \"chat_id\": 1}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 4\", \"chat_id\": 1}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 5\", \"chat_id\": 1}");

        
        MockEndpoint mock = getMockEndpoint("mock:chat_messages_grouped");
        
        mock.expectedMessageCount(3);
        
        assertMockEndpointsSatisfied();
        
        ObjectMapper mapper = new ObjectMapper();      

        // TODO: Get the values inside the exchange somehow and use the mapper to convert it to MessagesByUser and assert it
        
        LOG.info("TEST ********************************************************************************");
        LOG.info(mock.getExchanges().get(0).getIn().getBody().toString());
        LOG.info("TEST ********************************************************************************");        
    }

    @Override
    protected RoutesBuilder createRouteBuilder() {
        return new RouteBuilder() {
            @Override
            public void configure() {
        		from("direct:chat_messages")
        		.unmarshal().json(JsonLibrary.Jackson, ChatMessage.class) 
        		.aggregate(simple("${body.from_user}"), new MesssagesAggregationStrategy())
        		.completionSize(10)
        		.completionTimeout(1500)
        		.marshal().json(JsonLibrary.Jackson, MessagesByUser.class) 
        		.to("mock:chat_messages_grouped");
            }
        };
    }

}