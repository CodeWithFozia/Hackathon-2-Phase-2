import { useState, useCallback, useEffect } from 'react';
import { ChatMessage, ChatState } from '@/types/chat';
import { sendChatMessage, getChatHistory, clearChatHistory } from '@/lib/api/chat';
import { useAuth } from '@/lib/hooks/useAuth';

export function useChat() {
  const { user } = useAuth();
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
    isExpanded: false,
    hasUnread: false,
  });

  // Load chat history on mount
  useEffect(() => {
    if (user?.id) {
      loadHistory();
    }
  }, [user?.id]);

  const loadHistory = useCallback(async () => {
    if (!user?.id) return;

    try {
      const response = await getChatHistory(user.id);
      setState((prev) => ({
        ...prev,
        messages: response.messages,
        error: null,
      }));
    } catch (error) {
      console.error('Failed to load chat history:', error);
      setState((prev) => ({
        ...prev,
        error: 'Failed to load chat history',
      }));
    }
  }, [user?.id]);

  const sendMessage = useCallback(
    async (message: string) => {
      if (!user?.id || !message.trim()) return;

      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        const response = await sendChatMessage(user.id, message.trim());

        setState((prev) => ({
          ...prev,
          messages: response.messages,
          isLoading: false,
          hasUnread: !prev.isExpanded, // Mark as unread if chat is collapsed
        }));

        return response;
      } catch (error: any) {
        console.error('Failed to send message:', error);
        const errorMessage = error.response?.data?.detail?.message || 'Failed to send message';

        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));

        throw error;
      }
    },
    [user?.id, state.isExpanded]
  );

  const clearHistory = useCallback(async () => {
    if (!user?.id) return;

    try {
      await clearChatHistory(user.id);
      setState((prev) => ({
        ...prev,
        messages: [],
        error: null,
      }));
    } catch (error) {
      console.error('Failed to clear chat history:', error);
      setState((prev) => ({
        ...prev,
        error: 'Failed to clear chat history',
      }));
    }
  }, [user?.id]);

  const toggleExpanded = useCallback(() => {
    setState((prev) => ({
      ...prev,
      isExpanded: !prev.isExpanded,
      hasUnread: false, // Clear unread when expanding
    }));
  }, []);

  const setExpanded = useCallback((expanded: boolean) => {
    setState((prev) => ({
      ...prev,
      isExpanded: expanded,
      hasUnread: expanded ? false : prev.hasUnread, // Clear unread when expanding
    }));
  }, []);

  return {
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    isExpanded: state.isExpanded,
    hasUnread: state.hasUnread,
    sendMessage,
    loadHistory,
    clearHistory,
    toggleExpanded,
    setExpanded,
  };
}
