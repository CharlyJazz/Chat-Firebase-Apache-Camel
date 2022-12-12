package com.service.bus.apachecamelservicebus.routes;

import java.util.ArrayList;

public class MessagesByUser {
	private String from_user;
	private String chat_id;

	private ArrayList<ChatMessage> list_of_messages;
	
	public MessagesByUser() {
		
	}
	
	public MessagesByUser(String from_user, String chat_id, ChatMessage first_message) {
		super();
		this.from_user = from_user;
		this.chat_id = chat_id;
		this.list_of_messages = new ArrayList<ChatMessage>();
		this.list_of_messages.add(first_message);
	}
	
	public void addMessage(ChatMessage message) {
		this.list_of_messages.add(message);
	}

	public ArrayList<ChatMessage> getList_of_messages() {
		return list_of_messages;
	}

	public void setList_of_messages(ArrayList<ChatMessage> list_of_messages) {
		this.list_of_messages = list_of_messages;
	}

	public String getFrom_user() {
		return from_user;
	}

	public void setFrom_user(String from_user) {
		this.from_user = from_user;
	}
	
	public String getChat_id() {
		return chat_id;
	}

	public void setChat_id(String chat_id) {
		this.chat_id = chat_id;
	}
}
