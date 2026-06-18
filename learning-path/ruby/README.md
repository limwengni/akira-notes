# Ruby on Rails Learning Path — Beginner

> 1–2 hours/day · Learn Ruby first, then Rails on top of it

---

## Day 1 — Ruby Basics
**Goal:** get comfortable with the language before touching Rails

- Variables, strings, integers, booleans
- Arrays and hashes (Ruby's version of lists and dicts)
- Loops: `each`, `map`, `select`
- Methods: `def`, return values, default params
- String interpolation: `"Hello #{name}"`

**Practice:** write a small script — given an array of numbers, return only the even ones doubled.

Resources:
- [try.ruby-lang.org](https://try.ruby-lang.org) — interactive browser playground
- [ruby-lang.org/en/documentation](https://www.ruby-lang.org/en/documentation/)

---

## Day 2 — OOP in Ruby
**Goal:** understand how Ruby thinks about objects (everything is an object)

- Classes and `initialize`
- Instance variables (`@name`) vs class variables (`@@count`)
- Inheritance with `<`
- Modules and mixins (`include`)
- `attr_accessor`, `attr_reader`, `attr_writer`

**Practice:** create a `User` class with a name and email, and a `Admin` class that inherits from it.

---

## Day 3 — Intro to Rails + Project Structure
**Goal:** understand MVC and what Rails generates for you

```bash
gem install rails
rails new myapp
cd myapp
rails server
```

Understand the folders:
- `app/models/` — data logic
- `app/controllers/` — handles requests
- `app/views/` — HTML templates
- `config/routes.rb` — URL mapping
- `db/` — database stuff

**Focus:** Rails is "convention over configuration" — it makes a lot of decisions for you. Trust the structure.

---

## Day 4 — Routes, Controllers, Views
**Goal:** handle a request from URL to response

- Define a route in `config/routes.rb`
- Create a controller: `rails generate controller Pages home`
- Render a view (`.html.erb` — HTML with embedded Ruby)
- Pass data from controller to view with instance variables (`@posts`)

**Practice:** build a simple page that displays a hardcoded list of items.

---

## Day 5 — Models + Database (ActiveRecord)
**Goal:** persist data with almost zero SQL

- Generate a model: `rails generate model Post title:string body:text`
- Run migration: `rails db:migrate`
- ActiveRecord basics: `Post.all`, `Post.find(1)`, `Post.create(...)`, `.save`, `.destroy`
- Validations: `validates :title, presence: true`

**Practice:** wire up your list from Day 4 to pull from the database instead of being hardcoded.

---

## After the 5 days
- Full CRUD with scaffolding
- Authentication (Devise gem)
- REST API with Rails
- Background jobs (Sidekiq)
