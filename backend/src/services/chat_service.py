"""Chat service for AI-powered task management."""
import json
import logging
from typing import Optional, Dict, Any, List
from uuid import UUID
from groq import Groq
from sqlmodel import Session, select

from src.config import settings
from src.models.chat import ChatMessage
from src.api.routes.tasks import TaskService
from src.api.schemas.task import TaskCreate, TaskUpdate

logger = logging.getLogger(__name__)


class ChatService:
    """Service for processing chat messages and managing conversations."""

    def __init__(self, session: Session):
        self.session = session
        self.task_service = TaskService(session)
        self.groq_client = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None

    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """Get function definitions for Groq function calling."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional description of the task"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user, optionally filtered by completion status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "completed": {
                                "type": "boolean",
                                "description": "Filter by completion status (true for completed, false for pending, omit for all)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of tasks to return (default 20)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task (title, description, or completion status)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The UUID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description for the task"
                            },
                            "is_completed": {
                                "type": "boolean",
                                "description": "New completion status"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task permanently",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The UUID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    def save_message(
        self,
        user_id: UUID,
        role: str,
        content: str,
        message_metadata: Optional[Dict[str, Any]] = None
    ) -> ChatMessage:
        """Save a chat message to the database."""
        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
            message_metadata=message_metadata
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_history(self, user_id: UUID, limit: int = 50) -> List[ChatMessage]:
        """Retrieve chat history for a user."""
        query = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        messages = self.session.exec(query).all()
        return list(reversed(messages))  # Return in chronological order

    def clear_history(self, user_id: UUID) -> int:
        """Clear all chat history for a user."""
        messages = self.session.exec(
            select(ChatMessage).where(ChatMessage.user_id == user_id)
        ).all()
        count = len(messages)
        for message in messages:
            self.session.delete(message)
        self.session.commit()
        return count

    def execute_function(
        self,
        function_name: str,
        arguments: Dict[str, Any],
        user_id: UUID
    ) -> Dict[str, Any]:
        """Execute a function call from Groq."""
        try:
            if function_name == "create_task":
                task_data = TaskCreate(
                    title=arguments.get("title"),
                    description=arguments.get("description")
                )
                task = self.task_service.create_task(user_id, task_data)
                return {
                    "success": True,
                    "task": {
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed
                    }
                }

            elif function_name == "list_tasks":
                completed_filter = arguments.get("completed")
                limit = arguments.get("limit", 20)

                # Get tasks
                tasks_response = self.task_service.get_tasks(user_id, page=1, page_size=limit)
                tasks = tasks_response.items

                # Filter by completion status if specified
                if completed_filter is not None:
                    tasks = [t for t in tasks if t.is_completed == completed_filter]

                return {
                    "success": True,
                    "tasks": [
                        {
                            "id": str(t.id),
                            "title": t.title,
                            "description": t.description,
                            "is_completed": t.is_completed
                        }
                        for t in tasks
                    ],
                    "total": len(tasks)
                }

            elif function_name == "update_task":
                task_id = UUID(arguments.get("task_id"))
                task_data = TaskUpdate(
                    title=arguments.get("title"),
                    description=arguments.get("description"),
                    is_completed=arguments.get("is_completed")
                )
                task = self.task_service.update_task(user_id, task_id, task_data)
                return {
                    "success": True,
                    "task": {
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed
                    }
                }

            elif function_name == "delete_task":
                task_id = UUID(arguments.get("task_id"))
                self.task_service.delete_task(user_id, task_id)
                return {
                    "success": True,
                    "message": "Task deleted successfully"
                }

            else:
                return {
                    "success": False,
                    "error": f"Unknown function: {function_name}"
                }

        except Exception as e:
            logger.error(f"Error executing function {function_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def process_message(self, user_id: UUID, message: str) -> Dict[str, Any]:
        """Process a user message and return a response."""
        if not self.groq_client:
            return {
                "response": "Chat service is not configured. Please set GROQ_API_KEY.",
                "task_result": None,
                "messages": []
            }

        # Save user message
        user_msg = self.save_message(user_id, "user", message)

        # Get recent conversation history for context
        history = self.get_history(user_id, limit=10)

        # Build messages for Groq API
        groq_messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful task management assistant. You can help users create, "
                    "list, update, and delete tasks. Be concise and friendly. When you perform "
                    "an action, confirm it clearly. Use the provided functions to interact with tasks."
                )
            }
        ]

        # Add conversation history (excluding the current message we just saved)
        for msg in history[:-1]:
            groq_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # Add current user message
        groq_messages.append({
            "role": "user",
            "content": message
        })

        try:
            # Call Groq API with function calling
            response = self.groq_client.chat.completions.create(
                model=settings.groq_model,
                messages=groq_messages,
                tools=self.get_function_definitions(),
                tool_choice="auto",
                max_tokens=settings.groq_max_tokens,
                temperature=settings.groq_temperature
            )

            assistant_message = response.choices[0].message
            task_result = None

            # Check if the model wants to call a function
            if assistant_message.tool_calls:
                tool_call = assistant_message.tool_calls[0]
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute the function
                function_result = self.execute_function(function_name, function_args, user_id)
                task_result = function_result

                # Add function call to messages
                groq_messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": function_name,
                                "arguments": tool_call.function.arguments
                            }
                        }
                    ]
                })

                # Add function result
                groq_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(function_result)
                })

                # Get final response from model
                final_response = self.groq_client.chat.completions.create(
                    model=settings.groq_model,
                    messages=groq_messages,
                    max_tokens=settings.groq_max_tokens,
                    temperature=settings.groq_temperature
                )

                assistant_content = final_response.choices[0].message.content
            else:
                assistant_content = assistant_message.content

            # Save assistant response
            msg_metadata = {"function_call": function_name} if task_result else None
            self.save_message(user_id, "assistant", assistant_content, msg_metadata)

            # Get updated history
            updated_history = self.get_history(user_id, limit=50)

            return {
                "response": assistant_content,
                "task_result": task_result,
                "messages": updated_history
            }

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_response = f"I encountered an error: {str(e)}"
            self.save_message(user_id, "assistant", error_response)

            return {
                "response": error_response,
                "task_result": None,
                "messages": self.get_history(user_id, limit=50)
            }
