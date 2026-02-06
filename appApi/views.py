from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Cart, CartItem, Category, Product, Review 
from .serializers import CartItemSerializer, CartSerializer, CategoryDetailSerializer, CategoryListSerializer, ProductListSerializer, ProductDetailSerializer, ReviewSerializer


User = get_user_model()

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductListSerializer(
        products,
        many=True,
        context={"request": request}
    )
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, slug):
     product = Product.objects.get(slug=slug)
     serializer = ProductDetailSerializer(
        product,
        context={"request": request}
    )
     return Response(serializer.data)


@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerializer(
        category,
        context={"request": request}
    )
    return Response(serializer.data)


@api_view(["POST"])
def add_to_cart(request):
    cart_code = request.data.get("cart_code")
    product_id = request.data.get("product_id")

    cart, created = Cart.objects.get_or_create(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)
    cartitem.quantity = 1 
    cartitem.save() 

    serializer = CartSerializer(cart, context={"request": request})
    return Response(serializer.data)


@api_view(['PUT'])
def update_cartitem_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity"))

        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response(
            {"data": serializer.data, "message": "Cartitem updated successfully!"}
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=400
        )

   
@api_view(['DELETE'])
def delete_cartitem(request,pk):
    cartitem = CartItem.objects.get(id=pk)
    cartitem.delete()
    return Response("CartItem deleted successfully!", status=204)



@api_view(["POST"])
def add_review(request):
    
    product_id = request.data.get("product_id")
    email = request.data.get("email")
    rating = request.data.get("rating")
    review_text = request.data.get("review")

    product = Product.objects.get(id=product_id)
    user = User.objects.get(email=email)

    if Review.objects.filter(product=product, user=user).exists():
        return Response({"error": "You already dropped a review for this product"}, status=400)

    review  = Review.objects.create(product=product, user=user, rating=rating, review=review_text)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['GET'])
def product_search(request):
    query = request.query_params.get("query")
    if not query:
        return Response("No query provider", status=400)
    
    products = Product.objects.filter(Q(name__icontains=query) | 
                                      Q(description__icontains=query) |
                                      Q(category__name__icontains=query))
    serializer = ProductListSerializer(products, many=True, context={"request": request})
    return Response(serializer.data)
    