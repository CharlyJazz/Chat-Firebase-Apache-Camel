package com.service.bus.apachecamelservicebus;

import org.apache.camel.Exchange;
import org.apache.camel.RoutesBuilder;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.component.mock.MockEndpoint;
import org.apache.camel.model.dataformat.JsonLibrary;
import org.apache.camel.test.junit5.CamelTestSupport;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.service.bus.apachecamelservicebus.routes.ChatMessage;
import com.service.bus.apachecamelservicebus.routes.MessagesByUser;
import com.service.bus.apachecamelservicebus.routes.MesssagesAggregationStrategy;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ChatMessagesRouterJUnitTest extends CamelTestSupport {
    private static final Logger LOG = LoggerFactory.getLogger(CamelTestSupport.class);

    @Test
    public void testMock() throws Exception {

        template.sendBody("direct:chat_messages", "{\"from_user\": 1, \"to_user\": 2, \"body\": \"Hell 1 1th Group\", \"chat_id\": 1}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 1, \"to_user\": 2, \"body\": \"Hell 2 1th Group\", \"chat_id\": 1}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 1, \"to_user\": 2, \"body\": \"Hell 3 1th Group\", \"chat_id\": 1}");

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
                
        Exchange out = mock.getExchanges().get(0);
        
        MessagesByUser messages1 = out.getIn().getBody(MessagesByUser.class);
        
        assertEquals("Hell 1 1th Group", messages1.getList_of_messages().get(0));
        assertEquals("Hell 2 1th Group", messages1.getList_of_messages().get(1));
        assertEquals("Hell 3 1th Group", messages1.getList_of_messages().get(2));
        
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
        		.to("mock:chat_messages_grouped");
            }
        };
    }

}