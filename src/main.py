from typing import List

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

@strawberry.type
class SubTodo:
    subtitle: str

@strawberry.type
class Todo:
    id: int
    title: str
    subTodo: List[SubTodo]
    # limit: Datetime
    # priority: str
    # user_id: str

todos: List[Todo] = []

@strawberry.type
class Query:

    @strawberry.field
    def todo(self) -> List[Todo]:
        return todos

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_todo(self, title: str) -> Todo:
        new_todo = Todo(id=len(todos)+1, title=title, subTodo=[])
        todos.append(new_todo)
        return new_todo

    @strawberry.mutation
    def create_sub_todo(self, subtitle: str) -> SubTodo:
        new_sub_todo = SubTodo(subtitle=subtitle)

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app = FastAPI()

app.add_route('/graphql', graphql_app)
