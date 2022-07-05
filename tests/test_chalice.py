from apispec import APISpec
from chalice import Chalice

from chaliceapi.docs import Docs, Resp, Op
from chaliceapi.chalice import ChalicePlugin
from chaliceapi.pydantic import PydanticPlugin
from tests.schema import TestSchema, AnotherSchema


def setup_test():
    app = Chalice(app_name="test")
    spec = APISpec(
        title="Test Schema",
        openapi_version="3.0.1",
        version="0.0.0",
        chalice_app=app,
        plugins=[PydanticPlugin(), ChalicePlugin()],
    )
    return app, spec


# Test 1: make sure that this still works as-is.
def test_nothing():
    app, spec = setup_test()

    @app.route("/", methods=["GET"])
    def example_route():
        pass


# Test 2: test that we can get a response spec from only a model
def test_response_spec():
    app, spec = setup_test()

    @app.route(
        "/",
        methods=["GET"],
        docs=Docs(
            get=TestSchema,
        ),
    )
    def test():
        pass

    assert spec.to_dict() == {
        "paths": {
            "/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TestSchema"
                                    }
                                }
                            },
                        }
                    }
                }
            }
        },
        "info": {"title": "Test Schema", "version": "0.0.0"},
        "openapi": "3.0.1",
        "components": {
            "schemas": {
                "TestSchema": {
                    "title": "TestSchema",
                    "type": "object",
                    "properties": {
                        "hello": {"title": "Hello", "type": "string"},
                        "world": {"title": "World", "type": "integer"},
                    },
                    "required": ["hello", "world"],
                }
            }
        },
    }


# Test 3: test that we can get a response and request spec from only models
def test_request_response_spec():
    app, spec = setup_test()

    @app.route(
        "/test",
        methods=["GET", "POST"],
        docs=Docs(
            post=Op(
                request=TestSchema,
                response=AnotherSchema,
            )
        ),
    )
    def test():
        pass

    assert spec.to_dict() == {
        "paths": {
            "/test": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TestSchema"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/AnotherSchema"
                                    }
                                }
                            },
                        }
                    },
                }
            }
        },
        "info": {"title": "Test Schema", "version": "0.0.0"},
        "openapi": "3.0.1",
        "components": {
            "schemas": {
                "TestSchema": {
                    "title": "TestSchema",
                    "type": "object",
                    "properties": {
                        "hello": {"title": "Hello", "type": "string"},
                        "world": {"title": "World", "type": "integer"},
                    },
                    "required": ["hello", "world"],
                },
                "AnotherSchema": {
                    "title": "AnotherSchema",
                    "type": "object",
                    "properties": {
                        "nintendo": {"title": "Nintendo", "type": "string"},
                        "atari": {"title": "Atari", "type": "string"},
                    },
                    "required": ["nintendo", "atari"],
                },
            }
        },
    }


# Test 4: test that we can get a single response and request spec from a full Operation
def test_operation():
    app, spec = setup_test()

    @app.route(
        "/ops",
        methods=["GET", "POST"],
        docs=Docs(
            post=Op(
                request=AnotherSchema,
                response=Resp(
                    code=201, description="Updated successfully!", model=TestSchema
                ),
            )
        ),
    )
    def test():
        pass

    assert spec.to_dict() == {
        "paths": {
            "/ops": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/AnotherSchema"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Updated successfully!",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TestSchema"
                                    }
                                }
                            },
                        }
                    },
                }
            }
        },
        "info": {"title": "Test Schema", "version": "0.0.0"},
        "openapi": "3.0.1",
        "components": {
            "schemas": {
                "AnotherSchema": {
                    "title": "AnotherSchema",
                    "type": "object",
                    "properties": {
                        "nintendo": {"title": "Nintendo", "type": "string"},
                        "atari": {"title": "Atari", "type": "string"},
                    },
                    "required": ["nintendo", "atari"],
                },
                "TestSchema": {
                    "title": "TestSchema",
                    "type": "object",
                    "properties": {
                        "hello": {"title": "Hello", "type": "string"},
                        "world": {"title": "World", "type": "integer"},
                    },
                    "required": ["hello", "world"],
                },
            }
        },
    }


# Test 5: test that we can get summaries
def test_summaries():
    app, spec = setup_test()

    @app.route(
        "/summaries",
        methods=["GET"],
        docs=Docs(
            summary="This is a summary of an API request.",
        ),
    )
    def summary():
        pass

    assert spec.to_dict() == {
        "paths": {"/summaries": {"summary": "This is a summary of an API request."}},
        "info": {"title": "Test Schema", "version": "0.0.0"},
        "openapi": "3.0.1",
    }
