# Persistent Chat History

## Problem
`/rag/query` and `/rag/chat` generate responses but don't store them. Chat history is entirely ephemeral — backend discards it after each request, frontend stores it in `useState([])`. Switching API providers or restarting the server loses everything.

## Solution
Add SQLite-backed conversation persistence with full CRUD API and frontend conversation management UI.

---

## Backend Changes

### 1. Database Setup — `backend/app/models/database.py` (CREATE)

SQLAlchemy models + engine/session factory:

```python
class Conversation(Base):
    __tablename__ = "conversations"
    id: Column(String(36), primary_key=True)        # UUID
    title: Column(String(255), default="New Chat")
    created_at: Column(DateTime, default=utcnow)
    updated_at: Column(DateTime, default=utcnow, onupdate=utcnow)
    # relationship -> messages (cascade delete, order by created_at)

class ChatMessageModel(Base):
    __tablename__ = "chat_messages"
    id: Column(String(36), primary_key=True)        # UUID
    conversation_id: Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"))
    role: Column(String(10))                        # "user" | "assistant"
    content: Column(Text)
    sources_json: Column(Text, nullable=True)       # JSON-serialized sources
    created_at: Column(DateTime, default=utcnow)
```

Plus `engine`, `SessionLocal`, `get_db()` dependency, `init_db()`.

### 2. Config — `backend/app/utils/config.py` (MODIFY)

Add `database_url` property:
```python
@property
def database_url(self) -> str:
    return self.get_from_env("DATABASE_URL") or self.get("database.url", "sqlite:///./data/chat.db")
```

### 3. Config YAML — `backend/config.yaml` (MODIFY)

Add section:
```yaml
database:
  url: "sqlite:///./data/chat.db"
```

### 4. Schemas — `backend/app/models/schemas.py` (MODIFY)

Add to `ChatRequest`:
```python
conversation_id: Optional[str] = Field(None, description="Conversation ID for persistence")
```

Add to `ChatResponse`:
```python
conversation_id: Optional[str] = Field(None, description="Conversation ID")
```

New schemas: `ConversationCreateRequest`, `ConversationUpdateRequest`, `ConversationResponse`, `ConversationDetailResponse`, `ConversationListResponse`, `ChatMessageResponse`, `MessageListResponse`.

### 5. Models Init — `backend/app/models/__init__.py` (MODIFY)

Export new Pydantic schemas.

### 6. Conversation Service — `backend/app/services/conversation_service.py` (CREATE)

Methods:
- `list_conversations(limit, offset)` -> (list, total)
- `create_conversation(title)` -> Conversation
- `get_conversation(id)` -> Conversation | None
- `update_conversation(id, title)` -> Conversation | None
- `delete_conversation(id)` -> bool
- `add_message(conv_id, role, content, sources)` -> ChatMessageModel
- `get_messages(conv_id, limit, offset)` -> (list, total)
- `get_history_for_llm(conv_id)` -> list[dict] for pipeline

### 7. Conversations Router — `backend/app/api/conversations.py` (CREATE)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/conversations` | List conversations (limit, offset) |
| POST | `/conversations` | Create conversation |
| GET | `/conversations/{id}` | Get conversation + messages |
| PATCH | `/conversations/{id}` | Update title |
| DELETE | `/conversations/{id}` | Delete conversation |
| GET | `/conversations/{id}/messages` | Paginated messages |

### 8. Modified RAG Chat — `backend/app/api/rag.py` (MODIFY)

Flow:
1. If `conversation_id` provided and exists -> load history from DB
2. If `conversation_id` is None -> create new Conversation
3. Run RAG pipeline with resolved history
4. Persist user message + assistant message to DB
5. Return `conversation_id` in response

Backward compatible: old clients without `conversation_id` still work (creates new conversation automatically).

### 9. Deps — `backend/app/api/deps.py` (MODIFY)

Import and re-export `get_db` from `app.models.database`.

### 10. Main — `backend/main.py` (MODIFY)

- Import `conversations_router` from `app.api.conversations`
- Add `app.include_router(conversations_router)`
- Call `init_db()` in `lifespan()` startup

---

## Frontend Changes

### 11. Constants — `frontend/.../config/constants.js` (MODIFY)

Add conversation endpoints:
```javascript
CONVERSATIONS: '/conversations',
CONVERSATIONS_GET: (id) => `/conversations/${id}`,
CONVERSATIONS_DELETE: (id) => `/conversations/${id}`,
CONVERSATIONS_MESSAGES: (id) => `/conversations/${id}/messages`,
```

### 12. Conversations API — `frontend/.../services/api/conversations.js` (CREATE)

Methods: `list()`, `create(title)`, `get(id)`, `update(id, title)`, `delete(id)`, `getMessages(id)`.

### 13. HTTP Client — `frontend/.../services/api/client.js` (MODIFY)

Add `patch(url, data, options)` method (currently missing).

### 14. Conversation Store — `frontend/.../stores/conversationStore.js` (CREATE)

Class-based pub/sub store (same pattern as `uiStore.js`):
- State: `conversations[]`, `activeConversationId`, `loading`, `error`
- Actions: `loadConversations()`, `createConversation(title)`, `switchConversation(id)`, `deleteConversation(id)`, `renameConversation(id, title)`

### 15. Stores Index — `frontend/.../stores/index.js` (MODIFY)

Export `conversationStore`.

### 16. RAG API — `frontend/.../services/api/rag.js` (MODIFY)

Pass `conversation_id` in chat request body from options.

### 17. useChat Hook — `frontend/.../hooks/useChat.js` (MODIFY)

- Accept/manage `conversationId` state
- Send `conversation_id` in requests
- Store returned `conversation_id` from response
- Add `loadConversationMessages(id)` for hydration
- Add `createNewConversation()` replacing `clearChat`

### 18. Conversation List — `frontend/.../components/chat/ConversationList.jsx` (CREATE)

Sidebar panel: "New Chat" button, scrollable conversation list, active highlight, rename (inline edit), delete (with confirm).

### 19. Chat Page — `frontend/.../pages/Chat.jsx` (MODIFY)

New two-column layout:
```
+-------------------+----------------------------------------+
| ConversationList  |  Chat Area                             |
| (264px sidebar)   |  Header: [title] [rename]              |
|                   |  Messages (scrollable)                 |
|                   |  Input form                            |
+-------------------+----------------------------------------+
```

Integrate with `conversationStore` + updated `useChat`.

---

## File Summary

| # | File | Action |
|---|------|--------|
| 1 | `backend/app/models/database.py` | CREATE |
| 2 | `backend/app/utils/config.py` | MODIFY |
| 3 | `backend/config.yaml` | MODIFY |
| 4 | `backend/app/models/schemas.py` | MODIFY |
| 5 | `backend/app/models/__init__.py` | MODIFY |
| 6 | `backend/app/services/conversation_service.py` | CREATE |
| 7 | `backend/app/api/conversations.py` | CREATE |
| 8 | `backend/app/api/rag.py` | MODIFY |
| 9 | `backend/app/api/deps.py` | MODIFY |
| 10 | `backend/main.py` | MODIFY |
| 11 | `frontend/.../config/constants.js` | MODIFY |
| 12 | `frontend/.../services/api/conversations.js` | CREATE |
| 13 | `frontend/.../services/api/client.js` | MODIFY |
| 14 | `frontend/.../stores/conversationStore.js` | CREATE |
| 15 | `frontend/.../stores/index.js` | MODIFY |
| 16 | `frontend/.../services/api/rag.js` | MODIFY |
| 17 | `frontend/.../hooks/useChat.js` | MODIFY |
| 18 | `frontend/.../components/chat/ConversationList.jsx` | CREATE |
| 19 | `frontend/.../pages/Chat.jsx` | MODIFY |

## Bug Fix: SQLite Connection Error

The engine creation in `database.py` runs at **module import time**, but the `./data/` directory doesn't exist. This causes a SQLite error on startup.

**Fix:** `backend/app/models/database.py` — add `os.makedirs` before engine creation:

```python
import os
# ... existing imports ...

# Resolve database directory
_db_url = config.database_url
if "sqlite" in _db_url:
    # Extract path from sqlite:///./data/chat.db -> ./data/chat.db
    _db_path = _db_url.split("sqlite:///")[-1]
    _db_dir = os.path.dirname(_db_path)
    if _db_dir:
        os.makedirs(_db_dir, exist_ok=True)

engine = create_engine(...)
```

---

## Verification

1. Start backend: `cd backend && python main.py` — verify `data/chat.db` created
2. `POST /conversations` — creates conversation with UUID
3. `POST /rag/chat` with `conversation_id` — returns answer + same conversation_id
4. `GET /conversations/{id}` — shows conversation with messages
5. Refresh frontend `/chat` — conversation list loads, click to restore messages
6. Old behavior: `POST /rag/chat` without `conversation_id` — still works, auto-creates conversation
7. Create multiple conversations, switch between them, verify isolation
8. Delete conversation — removed from list and DB
