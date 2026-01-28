import apiClient from './client';
import { ChatMessageRequest, ChatResponse, ChatHistoryResponse } from '@/types/chat';

/**
 * Send a chat message and get AI response
 */
export async function sendChatMessage(
  userId: string,
  message: string
): Promise<ChatResponse> {
  const response = await apiClient.post<ChatResponse>(
    `/users/${userId}/chat`,
    { message } as ChatMessageRequest
  );
  return response.data;
}

/**
 * Get chat history for a user
 */
export async function getChatHistory(
  userId: string,
  limit: number = 50
): Promise<ChatHistoryResponse> {
  const response = await apiClient.get<ChatHistoryResponse>(
    `/users/${userId}/chat/history`,
    { params: { limit } }
  );
  return response.data;
}

/**
 * Clear all chat history for a user
 */
export async function clearChatHistory(userId: string): Promise<{ message: string; deleted_count: number }> {
  const response = await apiClient.delete<{ message: string; deleted_count: number }>(
    `/users/${userId}/chat/history`
  );
  return response.data;
}
