package com.service.bus.apachecamelservicebus.routes;

import java.util.ArrayList;

class MessagesByUser {
	private String user_id;
	private ArrayList<String> list_of_messages;
	
	public MessagesByUser() { // WHY?
		
	}
	
	public MessagesByUser(String user_id, String first_message) {
		super();
		this.user_id = user_id;
		this.list_of_messages = new ArrayList<String>();
		this.list_of_messages.add(first_message);
	}
	
	public void addMessage(String message) {
		this.list_of_messages.add(message);
	}

	public String getUser_id() {
		return user_id;
	}
	public void setUser_id(String user_id) {
		this.user_id = user_id;
	}
	public ArrayList<String> getList_of_messages() {
		return list_of_messages;
	}
	public void setList_of_messages(ArrayList<String> list_of_messages) {
		this.list_of_messages = list_of_messages;
	}
}