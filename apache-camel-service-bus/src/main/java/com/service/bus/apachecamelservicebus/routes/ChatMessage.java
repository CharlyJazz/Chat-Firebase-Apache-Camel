package com.service.bus.apachecamelservicebus.routes;

public class ChatMessage {
	private String from_user;
	private String to_user;
	private String chat_id;
	private String body;
	
	public ChatMessage() {
		
	}
	
	public ChatMessage(String from_user, String body, String to_user, String chat_id) {
		super();
		this.from_user = from_user;
		this.body = body;
		this.to_user = to_user;
		this.chat_id = chat_id;
	}

	public String getFrom_user() {
		return from_user;
	}

	public void setFrom_user(String from_user) {
		this.from_user = from_user;
	}

	public String getBody() {
		return body;
	}

	public void setBody(String message) {
		this.body = message;
	}

	public String getTo_user() {
		return to_user;
	}

	public void setTo_user(String to_user) {
		this.to_user = to_user;
	}

	public String getChat_id() {
		return chat_id;
	}

	public void setChat_id(String chat_id) {
		this.chat_id = chat_id;
	}
}
