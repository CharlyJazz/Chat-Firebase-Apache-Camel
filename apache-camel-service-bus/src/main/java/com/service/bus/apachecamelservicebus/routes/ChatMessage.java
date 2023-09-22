package com.service.bus.apachecamelservicebus.routes;

public class ChatMessage {
	private String from_user;
	private String to_user;
	private String chat_id;
	private String body;
	private String time;
	private String time_iso;
	private String message_id;
	
	public ChatMessage() {
		
	}
	
	public ChatMessage(String from_user, String body, String to_user, String chat_id, String time, String message_id, String time_iso) {
		super();
		this.chat_id = chat_id;
		this.from_user = from_user;
		this.to_user = to_user;
		this.message_id = message_id;
		this.body = body;
		this.time = time;
		this.time_iso = time_iso;
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

	public String getTime() {
		return time;
	}

	public void setTime(String time) {
		this.time = time;
	}

	public String getMessage_id() {
		return message_id;
	}

	public void setMessage_id(String message_id) {
		this.message_id = message_id;
	}

	public String getTime_iso() {
		return time_iso;
	}

	public void setTime_iso(String time_iso) {
		this.time_iso = time_iso;
	}
}
