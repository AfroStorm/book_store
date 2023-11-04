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


## To do
    1. Change the models so that each customer related model connects with #
        the user model as a central point. #
    2. Change serializers to correspond acordingly to new models. #
        Add to_representation methods to each serializer if necessary. #
            Restrict access to sensitive data. #
        Prevent owners from modifying data for which they have no #
            authorization. #
        Prevent unauthorized and authorized users from being able to set the #
            date_joined/last_login fields when creating a new user #
            (except staff) #
    3. Change permissions to corespond acordingly to different views. #
    4. create signals to create a product review history for #
        each product. #
    