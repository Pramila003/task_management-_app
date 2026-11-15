# Task Management API Route Guide

This guide documents the routes currently registered by `main.py`, including their request bodies, authentication requirements, declared success responses, and known implementation caveats.

## Run the API

From the project root, start the development server:

```powershell
python -m uvicorn main:app --reload
```

- Base URL: `http://127.0.0.1:8000`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

The application reads `DB_CONNECTION`, `SECRET_KEY`, `ALGORITHM`, and `EXP_TIME` from the environment or `.env` file. Do not share or commit secret values.

## Request and response conventions

- Send request bodies as JSON with the `Content-Type: application/json` header.
- Route paths below are relative to the base URL.
- Fields shown as `string`, `integer`, or `boolean` should use those JSON value types.
- The status codes below are the ones declared by the routes. Not every successful operation returns `200 OK`.

## Authentication

The API uses a JWT bearer token, not a separately supplied API key:

1. Register with `POST /user/register` if you do not already have an account.
2. Log in with `POST /user/login`.
3. Copy the `token` string from the login response.
4. For a protected request, send this HTTP header:

   ```text
   Authorization: Bearer <token>
   ```

Replace `<token>` with the token value only. Do not send the `.env` `SECRET_KEY`; that key is used by the server to sign and verify tokens. Tokens expire after the configured `EXP_TIME` (in minutes).

Currently, `POST /task/create` and `GET /user/is_auth` check this header. The other task routes do not currently require authentication. The authentication dependency is not declared as a FastAPI security scheme, so Swagger UI may not show an **Authorize** button; use an API client that lets you set the `Authorization` request header.

PowerShell example for logging in and calling the protected create route:

```powershell
$login = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/user/login" `
  -ContentType "application/json" `
  -Body (@{ username = "avery"; password = "choose-a-password" } | ConvertTo-Json)

$headers = @{ Authorization = "Bearer $($login.token)" }
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/task/create" `
  -Headers $headers `
  -ContentType "application/json" `
  -Body (@{
    title = "Prepare project report"
    description = "Collect the latest project updates"
    is_complete = $false
  } | ConvertTo-Json)
```

## User routes

### Register

`POST /user/register`

Authentication: none  
Declared success status: `201 Created`

Request body:

```json
{
  "name": "Avery Example",
  "username": "avery",
  "password": "choose-a-password",
  "email": "avery@example.com"
}
```

| Field | Type | Notes |
|---|---|---|
| `name` | string | Required by the request schema. |
| `username` | string | Supply this; accounts are checked for duplicate usernames. |
| `password` | string | Supply this; the server stores a password hash, not the submitted password. |
| `email` | string | Required by the request schema; duplicate emails are rejected. |

Declared success response:

```json
{
  "id": 1,
  "username": "avery"
}
```

The route also schedules an email task in the background.

Possible errors:

- `400 Bad Request` if the username or email already exists.
- `422 Unprocessable Entity` if required fields are missing or have invalid types.

### Log in

`POST /user/login`

Authentication: none  
Declared success status: `200 OK`

Request body:

```json
{
  "username": "avery",
  "password": "choose-a-password"
}
```

Supply both fields even though the current schema marks them optional.

Success response:

```json
{
  "token": "<jwt-token>"
}
```

Use the token in the `Authorization: Bearer <token>` header for protected routes.

Possible errors:

- `401 Unauthorized` with `{"detail":"wrong username"}` for an unknown username.
- `401 Unauthorized` with `{"detail":"wrong password"}` for a password that does not match.
- `422 Unprocessable Entity` for an invalid request body.

### Check the current token

`GET /user/is_auth`

Authentication: required. Send `Authorization: Bearer <token>`.  
Declared success status: `200 OK`

Request body: none.

The route returns the authenticated user object. The current implementation returns the database model directly; its fields can include `hash_password`. Treat this response as unsafe to expose, and do not publish or share its contents.

Possible errors:

- `401 Unauthorized` if the header is missing, is not in `Bearer <token>` format, the token is invalid, or the token has expired.

## Task routes

The task request schema has these fields:

| Field | Type | Notes |
|---|---|---|
| `title` | string or null | Task title. |
| `description` | string or null | Task description. |
| `is_complete` | boolean or null | Whether the task is complete. |

The current schema makes these fields optional. For task creation, provide all three fields to avoid creating a task with unintended null values.

The declared task response schema contains `id`, `title`, and `user_id`; it does not include `description` or `is_complete`.

### Create a task

`POST /task/create`

Authentication: required. Send `Authorization: Bearer <token>`.  
Declared success status: `201 Created`

Request body:

```json
{
  "title": "Prepare project report",
  "description": "Collect the latest project updates",
  "is_complete": false
}
```

Declared success response:

```json
{
  "id": 12,
  "title": "Prepare project report",
  "user_id": 1
}
```

The `user_id` is taken from the authenticated user, not from the request body.

Possible errors:

- `401 Unauthorized` if the bearer token is missing, invalid, or expired.
- `422 Unprocessable Entity` if the request body cannot be parsed.

### Get all tasks

`GET /task/all_task`

Authentication: none  
Declared success status: `200 OK`

Request body: none.

Declared success response:

```json
[
  {
    "id": 12,
    "title": "Prepare project report",
    "user_id": 1
  }
]
```

An empty task table returns an empty array: `[]`.

### Get one task

`GET /task/get_one_task/{task_id}`

Authentication: none  
Declared success status: `200 OK`

Replace `{task_id}` with the task's integer ID. Request body: none.

Declared success response:

```json
{
  "id": 12,
  "title": "Prepare project report",
  "user_id": 1
}
```

If the ID does not exist, the controller returns `404 Not Found`.
The error body is `{"detail":{"error code":"invalid task id"}}`.

### Update a task

`PUT /task/update_task/{task_id}`

Authentication: none  
Declared success status: `201 Created`

Replace `{task_id}` with the task's integer ID. Request body:

```json
{
  "title": "Prepare final project report",
  "description": "Include the latest project updates",
  "is_complete": true
}
```

This route assigns all three schema fields to the task. Include all fields; omitted fields can be set to null.

The route declares a `TaskResponseSchema` response, but the controller currently returns a `{ "status": ..., "data": ... }` object. Those shapes do not match, so this endpoint may fail response validation instead of returning the declared success response. The task ID is also returned as a `404 Not Found` when it does not exist.

### Partially update a task

`PUT /task/update_spec/{task_id}`

Authentication: none  
Declared success status: `201 Created`

Replace `{task_id}` with the task's integer ID. Only fields present in the JSON body are updated:

```json
{
  "is_complete": true
}
```

An empty object (`{}`) makes no field changes. The controller returns the task object, including its database fields. A typical response is:

```json
{
  "id": 12,
  "title": "Prepare final project report",
  "description": "Include the latest project updates",
  "is_complete": true,
  "user_id": 1
}
```

If the ID does not exist, the controller returns `404 Not Found`.
Its error body is `{"detail":{"error code":"no id "}}`.

### Delete a task

`DELETE /task/delete_task/{task_id}`

Authentication: none  
Declared success status: `204 No Content`

Replace `{task_id}` with the task's integer ID. Request body: none.

On success, the response has no body. If the ID does not exist, the controller returns `404 Not Found`.
The error body is `{"detail":{"error code":"no id"}}`.

## Known response caveats

- Routes with `response_model` return SQLAlchemy model instances, but the current Pydantic response schemas do not enable ORM attribute parsing (`from_attributes`). With Pydantic v2, this can cause response validation errors for registration and task routes even when the database operation succeeds.
- `PUT /task/update_task/{task_id}` has an additional mismatch: its controller returns a nested status/data object while its route declares a task response model.
- `GET /user/is_auth` returns the user database object directly, which may include the password hash. It should use a response schema that excludes sensitive fields.
- The routes declare `201 Created` for task updates; they do not declare `200 OK` for those operations.

These notes describe the current code, not recommended API design. Correcting these behaviors requires code changes separate from this route guide.
