# Models

## Tag
    Caption

## Category
    name<br>
    (Book, Magazine, Bookmarks, Educational Materials, Audiobooks)

## Product
    Category(foreign key)<br>
    name<br>
    image<br>
    Price<br>
    Description<br>
    Length<br>
    height<br>
    width<br>
    weight<br>
    Color<br>
    Rating<br>
    Publishing_date<br>
    Author<br>
    Tags(many to many)<br>

## Customer
    username<br>
    First_name<br>
    Last_name<br>
    Email<br>
    Date_joined

## Profile
    Customer(one to one)<br>
    Address<br>
    Wishlist<br>
    Purchase_history(many to many)<br>