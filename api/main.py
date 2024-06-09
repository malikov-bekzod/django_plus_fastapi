from fastapi import FastAPI, HTTPException,Depends,status
from .schemas import CategorySchema, ProductSchema, OrderSchema,JwtModel
from .crud import get_category, get_categories, get_product, get_products, get_order, get_orders
from web.models import Category,Product,Order
from fastapi_jwt_auth import AuthJWT
from django.contrib.auth.models import User
from werkzeug.security import check_password_hash
from fastapi.encoders import jsonable_encoder

app = FastAPI()

from fastapi import FastAPI, HTTPException
from typing import List
from .schemas import CategorySchema, ProductSchema, OrderSchema,LoginModel,RegisterModel
from .crud import get_category, get_categories, get_product, get_products, get_order, get_orders

app = FastAPI()


@AuthJWT.load_config
def config():
    return JwtModel()

@app.post("/register")
def register(user: RegisterModel):
    if User.objects.filter(username=user.username).exists():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if User.objects.filter(email=user.email).exists():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )
    new_user.set_password(user.password)
    new_user.save()

    data = {
        "success": True,
        "code": 201,
        "msg": "User successfully registered",
        "user": {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "username": new_user.username,
        }
    }
    return jsonable_encoder(data)

@app.post("/login")
def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    try:
        check_user = User.objects.get(username=user.username)
    except User.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    if check_user and check_user.check_password(user.password):
        access_token = Authorize.create_access_token(subject=check_user.username)
        refresh_token = Authorize.create_refresh_token(subject=check_user.username)
        data = {
            "success": True,
            "code": 200,
            "msg": "Success Login",
            "token": {
                "access_token": access_token,
                "refresh_token": refresh_token
            },
            "user":{
                "id":check_user.id,
                "first_name":check_user.first_name,
                "last_name":check_user.last_name,
                "email":check_user.email,
                "username":check_user.username,
            }
        }
        return jsonable_encoder(data)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

@app.get("/categories")
def read_categories():
    categories = get_categories()
    return categories

@app.post("/categories")
def create_category(category:CategorySchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="token need")
    new_category = Category(name=category.name, description=category.description)
    new_category.save()
    return {"msg": "category created"}


@app.get("/categories/{category_id}")
def read_category(category_id: int):
    category = get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.get("/products")
def read_products():
    products = get_products()
    return products

@app.get("/products/{product_id}")
def read_product(product_id: int):
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/orders")
def read_orders():
    orders = get_orders()
    return orders

@app.get("/orders/{order_id}")
def read_order(order_id: int):
    order = get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/products")
def create_product(product: ProductSchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token required")
    
    new_product = Product(name=product.name, description=product.description, price=product.price)
    new_product.save()

    for category_id in product.categories:
        category_instance = Category.objects.get(id=category_id)
        new_product.categories.add(category_instance)

    return {"msg": "Product created", "product": jsonable_encoder(new_product)}

@app.post("/orders")
def create_order(order: OrderSchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token required")
    
    try:
        user = User.objects.get(id=order.user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_order = Order(user=user, total_amount=order.total_amount)
    new_order.save()

    for product_id in order.products:
        product_instance = Product.objects.get(id=product_id)
        new_order.product.add(product_instance)

    return {"msg": "Order created", "order": jsonable_encoder(new_order)}