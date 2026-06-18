# Ruby on Rails Learning Path - Beginner

> 1-2 hours/day - Learn Ruby first, then let Rails make more sense on top of it.

---

## Day 1 - Ruby Basics
**Goal:** get comfortable with Ruby before touching Rails.

- Variables, strings, integers, booleans
- Arrays and hashes
- Loops: `each`, `map`, `select`
- Methods: `def`, return values, default params
- String interpolation: `"Hello #{name}"`

**Practice:** write a small script that takes an array of numbers and returns only the even numbers doubled.

**Keep it light:** if `map` or `select` feels confusing, rewrite the same solution with `each` first.

Resources:
- [try.ruby-lang.org](https://try.ruby-lang.org) - interactive browser playground
- [ruby-lang.org/en/documentation](https://www.ruby-lang.org/en/documentation/)

---

## Day 2 - OOP in Ruby
**Goal:** understand how Ruby thinks about objects.

- Classes and `initialize`
- Instance variables like `@name`
- `attr_accessor`, `attr_reader`, `attr_writer`
- Simple inheritance with `<`
- Modules and mixins (`include`) only as a quick preview

**Practice:** create a `User` class with a name and email, then create an `Admin` class that inherits from it.

**Keep it light:** do not spend too long on class variables like `@@count` yet. They are less important for beginner Rails work.

---

## Day 3 - Intro to Rails + Project Structure
**Goal:** create a Rails app and understand the main folders.

```bash
gem install rails
rails new myapp
cd myapp
bin/rails db:create
bin/rails server
```

Understand the folders:
- `app/models/` - data logic
- `app/controllers/` - handles requests
- `app/views/` - HTML templates
- `config/routes.rb` - URL mapping
- `db/` - database changes and schema

**Practice:** open the Rails welcome page in the browser, then find the folders above in your editor.

**Focus:** Rails is "convention over configuration". For now, trust the structure before trying to customize it.

---

## Day 4 - Routes, Controllers, Views
**Goal:** handle a request from URL to response.

- Define a route in `config/routes.rb`
- Create a controller: `bin/rails generate controller Pages home`
- Render a view (`.html.erb` - HTML with embedded Ruby)
- Pass data from controller to view with instance variables like `@items`

**Practice:** build a simple page that displays a hardcoded list of items.

**Keep it light:** do not connect the database yet. Today is only about request -> controller -> view.

---

## Day 5 - Models + Database (ActiveRecord)
**Goal:** persist data with very little SQL.

- Generate a model: `bin/rails generate model Post title:string body:text`
- Run migration: `bin/rails db:migrate`
- Try ActiveRecord basics in the console: `Post.all`, `Post.find(1)`, `Post.create(...)`, `.save`, `.destroy`
- Add one validation: `validates :title, presence: true`

**Practice:** change your Day 4 list so it pulls from the database instead of being hardcoded.

**Keep it light:** if the full page wiring feels too much, just create and read `Post` records in `bin/rails console`.

---

## After the 5 days
- Full CRUD with scaffolding
- Authentication
- REST API with Rails
- Background jobs
