// Chat type definitions

export interface ChatMessage {
  id: string;                          // UUID
  user_id: string;                     // User UUID
  role: 'user' | 'assistant';          // Message role
  content: string;                     // Message content
  message_metadata?: {                 // Optional metadata
    function_call?: string;
    task_id?: string;
    operation?: string;
  } | null;
  created_at: string;                  // ISO 8601 timestamp
}

export interface ChatMessageRequest {
  message: string;                     // User message (1-2000 chars)
}

export interface ChatResponse {
  response: string;                    // Assistant's response
  task_result?: {                      // Task operation result if applicable
    success?: boolean;
    task?: {
      id: string;
      title: string;
      description?: string;
      is_completed: boolean;
    };
    tasks?: Array<{
      id: string;
      title: string;
      description?: string;
      is_completed: boolean;
    }>;
    total?: number;
    message?: string;
    error?: string;
  } | null;
  messages: ChatMessage[];             // Updated conversation history
}

export interface ChatHistoryResponse {
  messages: ChatMessage[];             // List of messages
  total: number;                       // Total number of messages
}

export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  isExpanded: boolean;
  hasUnread: boolean;
}
