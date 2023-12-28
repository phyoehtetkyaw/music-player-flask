import sqlite3

conn = sqlite3.connect("db_music.sqlite")

cursor = conn.cursor()

sql = """
CREATE TABLE `tbl_albums` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `title` varchar(255) NOT NULL,
  `author_id` bigint NOT NULL,
  `description` longtext NOT NULL,
  `thumbnail` varchar(255) NOT NULL,
  `price` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_album_comments` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `user_id` bigint NOT NULL,
  `album_id` bigint NOT NULL,
  `comment` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_album_replies` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `user_id` bigint NOT NULL,
  `album_id` bigint NOT NULL,
  `comment_id` bigint NOT NULL,
  `reply` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_authors` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NOT NULL,
  `image` varchar(255) NOT NULL,
  `bio` text NOT NULL,
  `description` longtext NOT NULL,
  `genre_id` bigint NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_events` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `title` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `banner` varchar(255) NOT NULL,
  `start_datetime` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_event_ticket_rel` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `event_id` bigint NOT NULL,
  `ticket_id` bigint NOT NULL,
  `user_id` bigint NOT NULL
);

CREATE TABLE `tbl_genres` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_news` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `image` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_news_categories` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_news_comments` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `user_id` bigint NOT NULL,
  `news_id` bigint NOT NULL,
  `comment` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_news_replies` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `user_id` bigint NOT NULL,
  `news_id` bigint NOT NULL,
  `comment_id` bigint NOT NULL,
  `comment` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_products` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `price` int NOT NULL,
  `instock` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_product_images` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `product_id` bigint NOT NULL,
  `image` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_tickets` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `ticket_type` varchar(255) NOT NULL,
  `ticket_price` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_tracks` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `title` varchar(255) NOT NULL,
  `author_id` bigint NOT NULL,
  `album_id` bigint NOT NULL,
  `audio` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);

CREATE TABLE `tbl_users` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `username` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
);
"""

cursor.executescript(sql)