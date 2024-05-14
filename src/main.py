import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

@strawberry.type
class Todo:
    title: str
    # limit: Datetime
    # priority: str
    # user_id: str

@strawberry.type
class Query:

    @strawberry.field
    def todo(self) -> Todo:
        return Todo(title='first todo')

schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)

app = FastAPI()

app.add_route('/graphql', graphql_app)
