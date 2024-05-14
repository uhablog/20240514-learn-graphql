from typing import List

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

@strawberry.type
class Todo:
    title: str
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
        new_todo = Todo(title=title)
        todos.append(new_todo)
        return new_todo

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app = FastAPI()

app.add_route('/graphql', graphql_app)
