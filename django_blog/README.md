```
## Authentication System
```

You can copy this into your README and adjust wording slightly if you want.

---

# Authentication System Documentation

## Overview

The Django Blog application implements a secure user authentication system using Django’s built-in authentication framework. The system provides:

* User registration
* User login
* User logout
* Profile management
* Secure password handling
* Access control using login protection

The authentication system relies on Django’s built-in models, views, and password hashing mechanisms to ensure security and reliability.

---

## 1. User Registration

### How It Works

The registration system uses Django’s `UserCreationForm`, extended to include an email field.

When a user submits the registration form:

1. The form validates:

   * Username uniqueness
   * Password strength
   * Matching password confirmation
2. If valid, the user is saved to the database.
3. The password is automatically hashed using Django’s secure hashing algorithm (PBKDF2).
4. The user is redirected to the login page.

### Security

* Passwords are never stored in plain text.
* Django automatically hashes passwords using:

  ```
  pbkdf2_sha256
  ```
* CSRF protection is enforced using `{% csrf_token %}` in the registration form.

---

## 2. User Login

### How It Works

Login is handled using Django’s built-in `LoginView`.

When a user submits login credentials:

1. Django validates the username and password.
2. If valid, a session is created.
3. The user is redirected to the home page.
4. If invalid, an error message is displayed.

### Access Control

Protected pages use:

```python
@login_required
```

If a user attempts to access a protected page without authentication, they are redirected to:

```
/login/?next=...
```

---

## 3. User Logout

Logout is handled using Django’s built-in `LogoutView`.

When a user logs out:

1. The session is destroyed.
2. The user is redirected to the home page.
3. Protected routes become inaccessible until login.

---

## 4. Profile Management

### How It Works

Authenticated users can access:

```
/profile/
```

The profile page:

* Displays the username.
* Allows updating the email address.
* Uses a `ModelForm` bound to `request.user`.

When the form is submitted:

1. The form validates input.
2. The user instance is updated.
3. The page redirects to prevent resubmission.

### Security

* The profile view is protected with `@login_required`.
* CSRF token is included in the form.
* Only the logged-in user can modify their own information.

---

## 5. CSRF Protection

All POST forms include:

```html
{% csrf_token %}
```

This prevents Cross-Site Request Forgery attacks by ensuring that form submissions originate from the authenticated session.

---

## 6. Password Security

Passwords are securely handled by Django’s authentication system:

* Stored as hashed values.
* Not reversible.
* Verified using Django’s authentication backend.
* Visible in admin as:

```
algorithm: pbkdf2_sha256
iterations: ...
salt: ...
hash: ...
```

Raw passwords are never accessible.

---

# Testing Instructions

## Registration Testing

1. Navigate to:

   ```
   /register/
   ```
2. Create a new user.
3. Open:

   ```
   /admin/
   ```
4. Verify the user appears.
5. Confirm password is hashed (not plain text).

---

## Login Testing

1. Enter incorrect password → login must fail.
2. Enter correct password → login must succeed.
3. Visit:

   ```
   /profile/
   ```

   Access should be allowed.

---

## Logout Testing

1. Click logout.
2. Attempt to access:

   ```
   /profile/
   ```
3. You should be redirected to login.

---

## Profile Update Testing

1. Login.
2. Go to:

   ```
   /profile/
   ```
3. Update email.
4. Save.
5. Refresh page.
6. Confirm email persists.
7. Verify in admin panel.

---

# Access Control Testing

Open a private browser window.

Try accessing:

```
/profile/
```

Expected result:
Redirect to login page.

---

# Conclusion

The authentication system is:

* Secure
* CSRF protected
* Password hashed
* Access controlled
* Fully integrated with Django’s authentication framework




# Blog Post Management (CRUD)

## Overview

The Django Blog application implements full CRUD functionality for blog posts using Django’s class-based views. The system allows authenticated users to create posts, while ensuring that only the original author can edit or delete their content.

The following class-based views were used:

* `ListView`
* `DetailView`
* `CreateView`
* `UpdateView`
* `DeleteView`

---

## 1. Viewing Posts (Read Operations)

### Post List

URL:

```
/posts/
```

Description:

* Displays all blog posts.
* Posts are ordered by newest first.
* Shows:

  * Title
  * Truncated content preview
  * Author
  * Publication date
* Each title links to the full post detail page.

Access Level:
Public (no authentication required).

---

### Post Detail

URL:

```
/posts/<post_id>/
```

Description:

* Displays the full content of a single post.
* Shows:

  * Title
  * Full content
  * Author
  * Publication date
* Displays Edit and Delete links only if the logged-in user is the author.

Access Level:
Public viewing.
Edit/Delete links restricted to author.

---

## 2. Creating Posts

URL:

```
/posts/new/
```

Description:

* Allows authenticated users to create a new blog post.
* Uses a Django ModelForm.
* Author is automatically assigned as the logged-in user.

Security Implementation:

* Protected using `LoginRequiredMixin`.
* The `author` field is not exposed in the form.
* Author is set in the view using:

```python
form.instance.author = self.request.user
```

Redirect Behavior:

* After successful creation, the user is redirected to the post detail page using `get_absolute_url()`.

---

## 3. Updating Posts

URL:

```
/posts/<post_id>/edit/
```

Description:

* Allows authors to edit their posts.
* Uses the same ModelForm as post creation.

Security Implementation:

* Protected using:

  * `LoginRequiredMixin`
  * `UserPassesTestMixin`
* The `test_func()` method ensures:

```python
return self.request.user == post.author
```

Only the original author can edit the post.

Unauthorized users receive a 403 Forbidden response.

---

## 4. Deleting Posts

URL:

```
/posts/<post_id>/delete/
```

Description:

* Allows authors to delete their posts.
* Displays a confirmation page before deletion.

Security Implementation:

* Protected using:

  * `LoginRequiredMixin`
  * `UserPassesTestMixin`
* Only the author can delete their own post.
* Non-authors receive a 403 Forbidden response.

After deletion, users are redirected to:

```
/posts/
```

---

## 5. Model Configuration

The Post model includes:

* title
* content
* published_date (auto-generated)
* author (ForeignKey to User)

The model implements:

```python
def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})
```

This allows automatic redirection after creating or updating posts.

---

## 6. Permissions and Access Control

The system enforces the following rules:

| Action      | Authentication Required | Author Only |
| ----------- | ----------------------- | ----------- |
| View Posts  | No                      | No          |
| View Detail | No                      | No          |
| Create Post | Yes                     | No          |
| Edit Post   | Yes                     | Yes         |
| Delete Post | Yes                     | Yes         |

Security mechanisms used:

* `LoginRequiredMixin`
* `UserPassesTestMixin`
* Conditional template rendering
* CSRF protection on all forms

---

## 7. Data Handling and Validation

* Forms use Django’s ModelForm for validation.
* Required fields are enforced automatically.
* Author assignment is handled server-side.
* All POST forms include CSRF tokens.
* Invalid object IDs return 404 errors.

---

## 8. Testing Instructions

To test blog post features:

1. Login as a user.
2. Create a new post at `/posts/new/`.
3. Verify it appears in `/posts/`.
4. Click the title to view full content.
5. Edit the post and verify changes.
6. Delete the post and confirm removal.
7. Logout and verify:

   * Cannot create posts.
   * Cannot edit/delete posts.
8. Login as a different user and verify:

   * Cannot edit/delete another user's post.

---

## Conclusion

The blog post management system:

* Implements full CRUD functionality.
* Enforces strict ownership rules.
* Protects write operations with authentication.
* Uses Django best practices for redirection and validation.



# Comment System

## Overview

The Django Blog project includes a fully functional comment system that allows users to interact with blog posts. Users can:

* View comments under each blog post
* Add new comments (authenticated users only)
* Edit their own comments
* Delete their own comments

The system is implemented using Django’s `ModelForm` and class-based generic views with proper permission enforcement.

---

## Comment Model

The `Comment` model is defined in `blog/models.py`.

Fields:

* `post` – ForeignKey to `Post`
* `author` – ForeignKey to `User`
* `content` – TextField
* `created_at` – DateTimeField (auto_now_add=True)
* `updated_at` – DateTimeField (auto_now=True)

Example:

```python
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Relationship

* A post can have multiple comments.
* If a post is deleted, all associated comments are deleted automatically.
* Comments are accessed using:

```python
post.comments.all()
```

---

## Adding a Comment

URL pattern:

```
/posts/<post_id>/comments/new/
```

Rules:

* User must be logged in.
* The `post` is determined from the URL.
* The `author` is automatically assigned as the logged-in user.
* Users cannot manually assign the author or post.

After submission, the user is redirected to the related post detail page.

Security:

* Protected using `LoginRequiredMixin`
* CSRF protection enabled
* Server-side assignment of post and author

---

## Editing a Comment

URL pattern:

```
/comments/<comment_id>/update/
```

Rules:

* Only the original comment author can edit the comment.
* Enforced using `UserPassesTestMixin`.

Authorization check:

```python
def test_func(self):
    comment = self.get_object()
    return self.request.user == comment.author
```

If another user attempts to edit the comment, Django returns a 403 Forbidden response.

---

## Deleting a Comment

URL pattern:

```
/comments/<comment_id>/delete/
```

Rules:

* Only the comment author can delete the comment.
* A confirmation page is displayed before deletion.
* Protected using:

  * `LoginRequiredMixin`
  * `UserPassesTestMixin`

After deletion, the user is redirected back to the associated post.

---

## Displaying Comments

Comments are displayed on the post detail page.

Each comment shows:

* Content
* Author username
* Creation date

Edit and Delete links are shown only if:

```python
user == comment.author
```

If no comments exist, the page displays:

```
No comments yet.
```

---

## Permission Summary

| Action         | Login Required | Author Only |
| -------------- | -------------- | ----------- |
| View comments  | No             | No          |
| Add comment    | Yes            | No          |
| Edit comment   | Yes            | Yes         |
| Delete comment | Yes            | Yes         |

---

## Testing Instructions

To test the comment system:

1. Log in as a user.
2. Open a blog post.
3. Add a comment.
4. Confirm it appears under the post.
5. Edit the comment and confirm changes.
6. Delete the comment and confirm removal.
7. Log out and verify:

   * You cannot add comments.
   * Edit/Delete options are hidden.
8. Log in as another user and verify:

   * You cannot edit or delete someone else's comment.

