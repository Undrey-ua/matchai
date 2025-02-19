# Database Structure

## Tables

### Users
- `id`: Integer, Primary Key
- `email`: String, Unique, Indexed
- `full_name`: String
- `hashed_password`: String
- `interests`: Array[String]
- `is_active`: Boolean
- `age`: Integer, Nullable
- `location`: String, Nullable
- `social_links`: Array[String]
- `interest_vector`: Array[Float]
- `last_update`: DateTime

### Posts
- `id`: Integer, Primary Key
- `user_id`: Integer, Foreign Key -> Users
- `content`: Text
- `source`: String (facebook, twitter, etc.)
- `created_at`: DateTime

### Likes
- `id`: Integer, Primary Key
- `user_id`: Integer, Foreign Key -> Users
- `post_id`: Integer, Foreign Key -> Posts
- `created_at`: DateTime

### Matches
- `id`: Integer, Primary Key
- `user_id`: Integer, Foreign Key -> Users
- `matched_user_id`: Integer, Foreign Key -> Users
- `similarity_score`: Float
- `created_at`: DateTime

## Relationships
- User -> Posts: One-to-Many
- User -> Likes: One-to-Many
- User -> Matches: One-to-Many
- Post -> Likes: One-to-Many

## Indexes
- `users.email`: Unique index for quick user lookup
- `users.id`: Primary key index
- `posts.id`: Primary key index
- `likes.id`: Primary key index
- `matches.id`: Primary key index

## Usage
This database structure supports:
1. User registration and authentication
2. Social media data collection (posts)
3. User interaction tracking (likes)
4. Match recommendations storage
5. Interest vector storage for AI matching 