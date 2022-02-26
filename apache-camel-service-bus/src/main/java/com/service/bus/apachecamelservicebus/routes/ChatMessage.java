package com.service.bus.apachecamelservicebus.routes;

class ChatMessage {
	private String user_id;
	private String message;
	
	public ChatMessage() { // WHY?
		
	}
	
	public ChatMessage(String user_id, String message) {
		super();
		this.user_id = user_id;
		this.message = message;
	}

	public String getUser_id() {
		return user_id;
	}

	public void setUser_id(String user_id) {
		this.user_id = user_id;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}
	
	
}