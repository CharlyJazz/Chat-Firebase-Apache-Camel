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

        template.sendBody("direct:chat_messages", "{\"from_user\": 1, \"to_user\": 2, \"body\": \"Hell 1 1th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-01T21:17:12.074622\"}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 1, \"to_user\": 2, \"body\": \"Hell 2 1th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-02T21:17:12.074622\"}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 1, \"to_user\": 2, \"body\": \"Hell 3 1th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-03T21:17:12.074622\"}");

        template.sendBody("direct:chat_messages", "{\"from_user\": 2, \"to_user\": 2, \"body\": \"Hell 1 2th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-01T21:17:12.074622\"}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 2, \"to_user\": 2, \"body\": \"Hell 2 2th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-09T21:17:12.074622\"}");
        
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 1 3th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-01T21:17:12.074622\"}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 2 3th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-22T21:17:12.074622\"}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 3 3th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-20T21:17:12.074622\"}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 4 3th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-01T21:17:12.074622\"}");
        template.sendBody("direct:chat_messages", "{\"from_user\": 3, \"to_user\": 2, \"body\": \"Hell 5 3th Group\", \"chat_id\": 1, \"time_iso\": \"2023-10-01T21:17:12.074622\"}");

        
        MockEndpoint mock = getMockEndpoint("mock:chat_messages_grouped");

        mock.expectedMessageCount(1);
        
        assertMockEndpointsSatisfied();
                
        Exchange group_1 = mock.getExchanges().get(0);
        
        MessagesByUser messages1 = group_1.getIn().getBody(MessagesByUser.class);
        
        assertEquals("Hell 1 1th Group", messages1.getList_of_messages().get(0).getBody());
        assertEquals("Hell 2 1th Group", messages1.getList_of_messages().get(1).getBody());
        assertEquals("Hell 3 1th Group", messages1.getList_of_messages().get(2).getBody());
        assertEquals("2023-10-03T21:17:12.074622", messages1.getLatest_message_time_iso());
        
        Exchange group_2 = mock.getExchanges().get(1);
        
        MessagesByUser messages2 = group_2.getIn().getBody(MessagesByUser.class);
        
        assertEquals("Hell 1 2th Group", messages2.getList_of_messages().get(0).getBody());
        assertEquals("Hell 2 2th Group", messages2.getList_of_messages().get(1).getBody());
        assertEquals("2023-10-09T21:17:12.074622", messages2.getLatest_message_time_iso());
        
        Exchange group_3 = mock.getExchanges().get(2);
        
        MessagesByUser messages3 = group_3.getIn().getBody(MessagesByUser.class);
        

        assertEquals("Hell 1 3th Group", messages3.getList_of_messages().get(0).getBody());
        assertEquals("Hell 2 3th Group", messages3.getList_of_messages().get(1).getBody());
        assertEquals("Hell 3 3th Group", messages3.getList_of_messages().get(2).getBody());
        assertEquals("Hell 4 3th Group", messages3.getList_of_messages().get(3).getBody());
        assertEquals("Hell 5 3th Group", messages3.getList_of_messages().get(4).getBody());
        assertEquals("2023-10-22T21:17:12.074622", messages3.getLatest_message_time_iso());
    }

    @Override
    protected RoutesBuilder createRouteBuilder() {
        return new RouteBuilder() {
            @Override
            public void configure() {
        		from("direct:chat_messages")
        		.unmarshal().json(JsonLibrary.Jackson, ChatMessage.class) 
        		.aggregate(simple("${body.from_user}-${body.chat_id}"), new MesssagesAggregationStrategy())
        		.completionSize(10)
        		.completionTimeout(1500)
        		.to("mock:chat_messages_grouped");
            }
        };
    }

}