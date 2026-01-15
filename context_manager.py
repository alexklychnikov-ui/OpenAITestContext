from typing import Dict, List
from config import MAX_CONTEXT_MESSAGES

class ContextManager:
    def __init__(self):
        self.contexts: Dict[int, List[Dict[str, str]]] = {}
    
    def get_context(self, user_id: int) -> List[Dict[str, str]]:
        """Получить контекст пользователя"""
        context = self.contexts.get(user_id, [])
        if len(context) > MAX_CONTEXT_MESSAGES:
            context = context[-MAX_CONTEXT_MESSAGES:]
            self.contexts[user_id] = context
        return context
    
    def add_message(self, user_id: int, role: str, content: str):
        """Добавить сообщение в контекст"""
        if user_id not in self.contexts:
            self.contexts[user_id] = []
        
        self.contexts[user_id].append({
            "role": role,
            "content": content
        })
    
    def clear_context(self, user_id: int):
        """Очистить контекст пользователя"""
        if user_id in self.contexts:
            self.contexts[user_id] = []
    
    def update_context(self, user_id: int, user_message: str, assistant_message: str):
        """Обновить контекст после ответа бота"""
        self.add_message(user_id, "user", user_message)
        self.add_message(user_id, "assistant", assistant_message)
