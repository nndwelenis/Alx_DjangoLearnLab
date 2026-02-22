## Task 1 – Posts and Comments API Documentation

### Authentication

All posts and comments endpoints require Token Authentication.

Include this header in every request:

Authorization: Token <your_token>

Example:

Authorization: Token 4f9a8e7c6d5b4a3...

If the token is missing or invalid, the API returns:

{
  "detail": "Authentication credentials were not provided."
}

---

# Posts Endpoints

Base URL:

/api/posts/

---

## 1. Create Post

**Method:** POST  
**URL:** /api/posts/

### Request Body

{
  "title": "My first post",
  "content": "Hello world"
}

### Behavior

- The authenticated user is automatically set as the author.
- The author field cannot be manually assigned.
- The post is saved in the database.

### Success Response (201 Created)

{
  "id": 1,
  "author": 1,
  "author_username": "jay",
  "title": "My first post",
  "content": "Hello world",
  "created_at": "2026-02-22T13:10:00Z",
  "updated_at": "2026-02-22T13:10:00Z",
  "comments": []
}

---

## 2. List Posts (Paginated)

**Method:** GET  
**URL:** /api/posts/

### Response (200 OK)

{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": 1,
      "author_username": "jay",
      "title": "My first post",
      "content": "Hello world",
      "created_at": "...",
      "updated_at": "...",
      "comments": []
    }
  ]
}

### Notes

- Results are paginated.
- Default page size is 10.
- Use ?page=2 to navigate pages.

---

## 3. Retrieve Single Post

**Method:** GET  
**URL:** /api/posts/<id>/

Example:

/api/posts/1/

Returns a single post including nested comments.

---

## 4. Update Post (Owner Only)

**Method:** PATCH  
**URL:** /api/posts/<id>/

### Request Body

{
  "content": "Updated content"
}

### Permission Rule

Only the author of the post can update it.

If another user attempts to update:

{
  "detail": "You do not have permission to perform this action."
}

---

## 5. Delete Post (Owner Only)

**Method:** DELETE  
**URL:** /api/posts/<id>/

Response:

204 No Content

Only the author can delete.

---

## 6. Search Posts

**Method:** GET  
**URL:** /api/posts/?search=hello

Searches within:
- title
- content

---

# Comments Endpoints

Base URL:

/api/comments/

---

## 1. Create Comment

**Method:** POST  
**URL:** /api/comments/

### Request Body

{
  "post": 1,
  "content": "Nice post!"
}

### Behavior

- Authenticated user is automatically assigned as author.
- Comment is linked to the specified post.

### Success Response

{
  "id": 1,
  "post": 1,
  "author": 1,
  "author_username": "jay",
  "content": "Nice post!",
  "created_at": "...",
  "updated_at": "..."
}

---

## 2. List Comments

**Method:** GET  
**URL:** /api/comments/

Returns paginated list of comments.

---

## 3. Retrieve Single Comment

**Method:** GET  
**URL:** /api/comments/<id>/

---

## 4. Update Comment (Owner Only)

**Method:** PATCH  
**URL:** /api/comments/<id>/

Only the author can update.

---

## 5. Delete Comment (Owner Only)

**Method:** DELETE  
**URL:** /api/comments/<id>/

Only the author can delete.

---

# Permission Rules Summary

| Action | Allowed Users |
|--------|--------------|
| View posts/comments | Any authenticated user |
| Create post/comment | Any authenticated user |
| Update post/comment | Only the author |
| Delete post/comment | Only the author |

---

# Technical Features Implemented

- ModelViewSet for full CRUD operations
- Custom permission class (IsOwnerOrReadOnly)
- Pagination (PageNumberPagination, page size 10)
- Search filtering on title and content
- Nested comments inside PostSerializer
- Automatic author assignment using perform_create()


---

````markdown
## Task 2 – User Follows and Feed Functionality

This phase enhances the Social Media API by implementing user follow relationships and a dynamic feed system. Users can now follow and unfollow other users, and retrieve a personalized feed containing posts from the users they follow.

---

### User Model Update

The custom User model includes a self-referencing ManyToMany field:

```python
following = models.ManyToManyField(
    "self",
    symmetrical=False,
    related_name="followers",
    blank=True
)
````

* `following` represents users that the current user follows.
* `followers` (via `related_name`) represents users who follow the current user.
* `symmetrical=False` ensures the relationship is one-directional.

---

## API Endpoints

All endpoints require token authentication.

Include this header in all requests:

```
Authorization: Token <your_token>
```

---

### 1. Follow a User

**Endpoint**

```
POST /api/accounts/follow/<user_id>/
```

**Description**

Adds the specified user to the authenticated user's following list.

**Example Response**

```json
{
  "detail": "You are now following userB."
}
```

If the user does not exist:

```json
{
  "detail": "User not found."
}
```

If attempting to follow yourself:

```json
{
  "detail": "You cannot follow yourself."
}
```

---

### 2. Unfollow a User

**Endpoint**

```
POST /api/accounts/unfollow/<user_id>/
```

**Description**

Removes the specified user from the authenticated user's following list.

**Example Response**

```json
{
  "detail": "You have unfollowed userB."
}
```

---

### 3. Feed Endpoint

**Endpoint**

```
GET /api/feed/
```

**Description**

Returns posts created by users that the authenticated user follows.

* Posts are ordered by newest first.
* Only accessible to authenticated users.

**Example Response**

```json
[
  {
    "id": 5,
    "title": "Post from userB",
    "content": "This should appear in feed.",
    "author": 8,
    "created_at": "2026-02-22T14:01:12Z",
    "updated_at": "2026-02-22T14:01:12Z"
  }
]
```

If the user does not follow anyone:

```json
[]
```

---

## Permissions

All follow, unfollow, and feed endpoints require authentication using Django REST Framework token authentication:

```
Authorization: Token <token>
```

Unauthenticated requests return:

```
401 Unauthorized
```

---

## Testing Procedure

1. Register two users.
2. Login both users and obtain tokens.
3. Create posts using the second user.
4. Follow the second user using the first user.
5. Retrieve `/api/feed/` using the first user.
6. Confirm posts appear in the feed.
7. Unfollow the second user.
8. Confirm the feed is empty again.

---

## Summary

This implementation introduces:

* Self-referencing follow relationships
* Secure follow and unfollow endpoints
* A personalized feed based on followed users
* Authentication enforcement across all social interactions

The Social Media API now supports core social networking behavior.

```
