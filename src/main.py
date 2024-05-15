from typing import List
from datetime import datetime
import uuid
import enum

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from strawberry.scalars import ID

@strawberry.enum
class Priority(enum.Enum):
    HIGH = "高い"
    MEDIUM = "中くらい"
    LOW = "低い"

@strawberry.type
class SubTodo:
    id: ID
    subtitle: str

@strawberry.type
class Todo:
    id: ID
    title: str
    limit: datetime
    priority: Priority
    subTodos: List[SubTodo] = strawberry.field(default_factory=list)

todos: List[Todo] = []

@strawberry.type
class Query:

    @strawberry.field
    def todo(self) -> List[Todo]:
        return todos

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_todo(self, title: str,
                    limit: datetime,
                    priority: Priority
                    ) -> Todo:
        new_todo = Todo(
                    id=strawberry.ID(str(uuid.uuid4())),
                    title=title,
                    limit=limit,
                    priority=priority
                   )
        todos.append(new_todo)
        return new_todo

    @strawberry.mutation
    def create_sub_todo(self, todo_id: strawberry.ID, subtitle: str) -> SubTodo:

        for todo in todos:
            if todo.id == todo_id:
                new_sub_todo = SubTodo(id=strawberry.ID(str(uuid.uuid4())), subtitle=subtitle)
                todo.subTodos.append(new_sub_todo)
                return new_sub_todo

        raise ValueError(f"Todo with ID {todo_id} not found")

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app = FastAPI()

app.add_route('/graphql', graphql_app)
