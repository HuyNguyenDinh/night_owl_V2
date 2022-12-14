from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.decorators import action
from rest_framework import status, generics, viewsets, permissions
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .perms import *
from .paginations import *
from django.db.models import Q, Sum, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from market.utils import *
from .mongo_connect import *
from threading import Thread
from market.speedSMS import *
from market.googleInfo import *
from rest_framework_simplejwt.tokens import RefreshToken
from chat.models import *
from django.utils import timezone
import uuid
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from asgiref.sync import async_to_sync
from .tasks import *
from django.core.exceptions import ValidationError
# Create your views here.


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    parser_classes = [MultiPartParser, JSONParser]
    pagination_class = None

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

    def get_serializer_class(self):
        if self.action == "balance_cashin":
            return UserCashinSerializer
        elif self.action == "login_with_google":
            return GoogleTokenSerializer
        elif self.action in ['check_verified_code_to_email', 'check_verified_code_to_phone_number']:
            return VerifiedCodeSerializer
        elif self.action in ['send_verified_code_to_email', 'send_verified_code_to_phone_number']:
            return MessageSerializer
        elif self.action == "reset_password":
            return ResetPasswordSerialier
        elif self.action == "change_password":
            return ChangePasswordSerializer
        elif self.action == "get_token_by_user_id_and_reset_code":
            return GetTokenWithUserIdAndCodeSerializer
        elif self.action == "create_single_chatroom":
            return RoomSerializer
        elif self.action == "change_avatar":
            return UserAvatarSerializer
        elif self.action == "get_user_id_with_email":
            return EmailSerializer
        elif self.action == 'get_shop_vouchers_available':
            return VoucherSerializer
        return UserSerializer

    @action(methods=['patch'], detail=False, url_path='change-avatar')
    def change_avatar(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.update_avatar(user, serializer.validated_data)
        return Response(UserLessInformationSerializer(user).data)

    @action(methods=['get'], detail=True, url_path='products')
    def product_of_user(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_business=True)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(ProductOfUserSerializer(user).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='change_password')
    def change_password(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if not current_password or not new_password or not confirm_password:
            return Response({"message": "current password, new password and confirm password are required"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if new_password != confirm_password:
            return Response({"message": "new password and confirm password are not the same"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            with transaction.atomic():
                user = User.objects.select_for_update().get(pk=request.user.id)
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                else:
                    raise Exception
        except:
            return Response({"message": "current password not correct or new password not match require case"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({"message": "change password successful"}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='get-user-id-with-email')
    def get_user_id_with_email(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(EmailSerializer({"user_id": user.id}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='send-reset-code-to-email')
    def send_reset_code_to_email(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            code = add_reset_code(user.id)
            subject = "X??c nh???n reset m???t kh???u c???a {0} Night Owl ECommerce".format(user.first_name)
            content = """M?? x??c minh ????? reset m???t kh???u Night Owl ECommerce c???a {0} l?? {1}""".format(user.first_name, code)
            send_email_task.delay(user.email, subject, content)
            return Response({"message": "reset code has been sent to your email"}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='get-token-by-user-id-and-reset-code')
    def get_token_by_user_id_and_reset_code(self, request):
        user_id = request.data.get('user_id')
        code = request.data.get('code')
        if check_reset_code(user_id, code):
            user = User.objects.get(pk=user_id)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "verification code was not correct"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='reset-password')
    def reset_password(self, request):
        try:
            User.objects.get(pk=request.user.id)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            if not new_password or not confirm_password:
                return Response({"message": 'new password and confirm password are required'}, status=status.HTTP_400_BAD_REQUEST)
            if new_password != confirm_password:
                return Response({"message": "new password and confirm password not the same"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            try:
                with transaction.atomic():
                    user_change = User.objects.select_for_update().get(pk=request.user.id)
                    user_change.set_password(new_password)
                    user_change.save()
            except:
                return Response({"message": "new password not match the requirement case"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                return Response({"message": "reset password successful"}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='send-verified-code-to-email')
    def send_verified_code_to_email(self, request):
        user = User.objects.get(pk=request.user.id, email_verified=False)
        if user:
            code = add_verified_code(user.id, True)
            subject = "X??c nh???n email ????ng k?? t??i kho???n t???i Night Owl"
            content = """Xin ch??o {0}, m?? x??c minh email ????ng k?? t??i kho???n t???i Night Owl c???a b???n l?? {1}.
            L??u ??: M?? x??c minh ch??? c?? hi???u l???c trong v??ng 15 ph??t.""".format(user.first_name, code)
            send_email_task.delay(user.email, subject, content)
            return Response({"message": "verification code has been sent, please check your email to get the code"})
        return Response({'message': "user not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, url_path='send-verified-code-to-phone-number')
    def send_verified_code_to_phone_number(self, request):
        user = User.objects.get(pk=request.user.id, phone_verified=False)
        if user:
            code = add_verified_code(user.id, False)
            content = """
                        Xin ch??o {0}, m?? x??c minh s??? ??i???n tho???i ????ng k?? t??i kho???n t???i Night Owl c???a b???n l?? {1}.
                        L??u ??: M?? x??c minh ch??? c?? hi???u l???c trong v??ng 15 ph??t.
                    """.format(user.first_name, code)
            send_sms(user.phone_number, content)
            return Response({"message": "verification code has been sent, please check your email to get the code"})
        return Response({'message': "user not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='check-verified-code-to-email')
    def check_verified_code_to_email(self, request):
        code = request.data.get('code')
        if check_verified_code(request.user.id, code, True):
            try:
                with transaction.atomic():
                    user = User.objects.select_for_update().get(pk=request.user.id)
                    user.email_verified = True
                    user.save()
            except:
                return Response({"message": "something wrong, please contact customer support to help"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "email verification successful"}, status=status.HTTP_200_OK)
        return Response({"message": "verification code was not correct"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['post'], detail=False, url_path='check-verified-code-to-phone-number')
    def check_verified_code_to_phone_number(self, request):
        code = request.data.get('code')
        if check_verified_code(request.user.id, code, False):
            try:
                with transaction.atomic():
                    user = User.objects.select_for_update().get(pk=request.user.id)
                    user.phone_verified = True
                    user.save()
            except:
                return Response({"message": "something wrong, please contact customer support to help"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "phone number verification successful"}, status=status.HTTP_200_OK)
        return Response({"message": "verification code was not correct"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        current_user = User.objects.get(pk=request.user.id)
        if current_user:
            return Response(UserSerializer(current_user).data, status=status.HTTP_200_OK)
        return Response({'message': "Current user not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='cashin')
    def balance_cashin(self, request):
        user = User.objects.get(pk=request.user.id)
        amount = request.data.get("amount")
        momo_collection = db_payment.momo
        payment_result = cashin_balance(user.id, amount, "https://night-owl-market-fe.vercel.app/payment")
        if payment_result and payment_result.get("resultCode") == 0:
            momo_collection.insert_one(payment_result)
            return Response({"message": "please go to the link below and pay for the order", "pay_url": payment_result.get("payUrl")}, status=status.HTTP_200_OK)
        return Response({"message": "something wrong with momo order"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='login-with-google')
    def login_with_google(self, request):
        idToken = request.data.get('id_token')
        if idToken:
            user_info = get_user_info(idToken)
            if user_info:
                user_email = user_info.get('email')
                try:
                    user = User.objects.get(email=user_email)
                except:
                    user_first_name = user_info.get('given_name')
                    user_last_name = user_info.get('family_name')
                    return Response(GoogleTokenSerializer({
                        "email": user_email, "first_name": user_first_name, "last_name": user_last_name
                    }).data, status=status.HTTP_302_FOUND)
                else:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
            return Response({"message": "User's info not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "id_token not found"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='single-chat')
    def create_single_chatroom(self, request, pk):
        try:
            chat_user = User.objects.get(pk=pk)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(pk=request.user.id)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_403_FORBIDDEN)
        single_room = Room.objects.filter(user=user, room_type=0).filter(user=chat_user).first()
        if single_room:
            return Response(RoomSerializer(single_room, context={"user": request.user.id}).data, status=status.HTTP_200_OK)
        else:
            single_room = Room.objects.create(group_name=f'roomchat_{str(uuid.uuid4())}')
            single_room.user.add(*[user, chat_user])
            return Response(RoomSerializer(single_room, context={"user": request.user.id}).data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True, url_path="vouchers-available")
    def get_shop_vouchers_available(self, request, pk):
        paginator = BasePagination()
        queryset = Voucher.objects.filter(Q(start_date__lte=timezone.now()) & (Q(end_date__gt=timezone.now()) | Q(end_date__isnull=True)) & Q(creator=pk))
        page = paginator.paginate_queryset(queryset=queryset, request=request)
        if page:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'login_with_google', "send_reset_code_to_email", "get_user_id_with_email",\
                           'product_of_user', 'get_token_by_user_id_and_reset_code', 'get_shop_vouchers_available']:
            return [permissions.AllowAny(), ]
        return [permissions.IsAuthenticated(), ]


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCreator]
    serializer_class = AddressSerializer

    def get_permissions(self):
        if action == 'create':
            return [permissions.IsAuthenticated(), ]
        return [IsCreator(), ]

    def get_queryset(self):
        return Address.objects.filter(creator__id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(creator=request.user)

            except:
                return Response({"message": "can not add more address because you still have address"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'message': 'cannot add address to your account'}, status=status.HTTP_400_BAD_REQUEST)


class CartDetailViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    pagination_class = None

    def get_queryset(self):
        return CartDetail.objects.filter(customer=self.request.user.id)

    @action(methods=['get'], detail=False, url_path='get-cart-groupby-owner')
    def get_cart_groupby_owner(self, request):
        cart = CartDetail.objects.filter(customer__id=request.user.id).all().values_list('id')
        owner = User.objects.filter(product__option__cartdetail__id__in=cart).distinct()
        carts = CartInStoreSerializer(owner, context={'request': request}, many=True)
        if carts:
            return Response(carts.data, status=status.HTTP_200_OK)
        return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class ProductViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser]
    pagination_class = BasePagination
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['sold_amount', 'owner']
    search_fields = ['name', 'owner__first_name', 'owner__last_name']
    ordering_fields = ['sold_amount']

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

    def get_permissions(self):
        if self.action in ["list", "retrieve", "get_comments", "get_options"]:
            return [permissions.AllowAny(), ]
        elif self.action == "get_vouchers_available_of_product":
            return [permissions.IsAuthenticated(), ]
        elif self.action == 'add_comment':
            return [VerifiedUserPermission(), ]
        elif self.action == 'create':
            return [BusinessPermission(), ]
        return [BusinessOwnerPermission(), ]

    def get_queryset(self):
        has_options = self.request.query_params.get('has_option')
        products = Product.objects.all()
        if self.action in ["update", "destroy", "add_option"]:
            products = products.filter(owner=self.request.user.id)
        elif self.action in ["list", "retrieve"]:
            if has_options and has_options == "0":
                pass
            else:
                products = products.filter(option__isnull=False).distinct()
        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            products = products.filter(categories=cate_id)
        return products

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductRetrieveSerializer
        elif self.action == 'add_comment':
            return CreateRatingSerializer
        elif self.action == 'add_option':
            return CreateOptionSerializer
        elif self.action == 'list':
            return ListProductSerializer
        elif self.action == 'get_vouchers_available_of_product':
            return VoucherSerializer
        return ProductSerializer

    @action(methods=['get'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        pd = Product.objects.get(pk=pk)
        comments = Rating.objects.filter(product=pd)
        paginator = CommentPagination()
        page = paginator.paginate_queryset(comments, request)
        if page:
            serializer = RatingSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response({'message': 'This product had no comment'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        pd = Product.objects.get(pk=pk)
        try:
            self.check_object_permissions(request, pd)
        except:
            return Response({'message': 'please login to comment'}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = CreateRatingSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save(creator=request.user, product=pd)
                except ValidationError as e:
                    return Response({'message': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': 'not valid comment'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['post'], detail=True, url_path='add-option')
    def add_option(self, request, pk):
        pd = Product.objects.get(pk=pk)
        try:
            self.check_object_permissions(request, pd)
        except:
            return Response({'message': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = CreateOptionSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(base_product=pd)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': "cannot add options to product"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='options')
    def get_options(self, request, pk):
        options = Product.objects.get(pk=pk).option_set.all()
        options = options.filter(unit_in_stock__gt=0)
        if options:
            return Response(OptionSerializer(options, many=True).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 2))
    @action(methods=['get'], detail=False, url_path='products-statistic-count-in-year')
    def products_statistic_in_year(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            year = request.query_params.get('year')
            order_details = OrderDetail.objects.filter(order__store=user)
            if year:
                try:
                    year = int(year)
                except:
                    return Response({"message": "year parameter was wrong format it must be in [0-9]"})
                else:
                    order_details = order_details.filter(order__order_date__year=year).select_related()
            else:
                order_details = order_details.filter(order__order_date__year=timezone.now().year).select_related()
            if order_details:
                product_count_weekday = order_details.values('order__order_date__week_day') \
                    .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__week_day')
                product_count_week = order_details.values('order__order_date__week') \
                    .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__week')
                product_count_month = order_details.values('order__order_date__month')\
                    .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__month')
                total_quantity_count = order_details.aggregate(total_quantity_count=Sum('quantity')).get(
                    'total_quantity_count')
                total_product_count = order_details.aggregate(
                    total_count=Count('product_option__base_product__id')).get('total_count')
                return Response({
                    "product_count_weekday": list(product_count_weekday),
                    "product_count_week": list(product_count_week),
                    "product_count_month": list(product_count_month),
                    "total_quantity_count": total_quantity_count,
                    "total_product_count": total_product_count
                }, status=status.HTTP_200_OK)
            return Response({"message": "order details not found"}, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 2))
    @action(methods=['get'], detail=False, url_path='products-statistic-count-in-month')
    def monthly_statistic_products_count(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            month = request.query_params.get('month')
            year = request.query_params.get('year')
            order_details = OrderDetail.objects.filter(order__store=user)
            if month:
                try:
                    month = int(month)
                except:
                    return Response({"message": "month parameter was wrong format it must be [0-12]"})
                else:
                    order_details = order_details.filter(order__order_date__month=month)
            else:
                order_details = order_details.filter(order__order_date__month=timezone.now().month)
            if year:
                try:
                    year = int(year)
                except:
                    return Response({"message": "year parameter was wrong format it must be [0-9]"})
                else:
                    order_details = order_details.filter(order__order_date__year=year).select_related()
            else:
                order_details = order_details.filter(order__order_date__year=timezone.now().year).select_related()
            if order_details:
                product_count_weekday = order_details.values('order__order_date__week_day')\
                    .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__week_day')
                product_count_week = order_details.values('order__order_date__week')\
                    .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__week')
                product_count_day = order_details.values('order__order_date__day')\
                    .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__day')
                total_quantity_count = order_details.aggregate(total_quantity_count=Sum('quantity')).get('total_quantity_count')
                total_product_count = order_details.aggregate(total_count=Count('product_option__base_product__id')).get('total_count')
                return Response({
                    "product_count_weekday": list(product_count_weekday),
                    "product_count_week": list(product_count_week),
                    "product_count_day": list(product_count_day),
                    "total_quantity_count": total_quantity_count,
                    "total_product_count": total_product_count
                }, status=status.HTTP_200_OK)
            return Response({"message": "order details not found"}, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 2))
    @action(methods=['get'], detail=True, url_path='product-statistic-in-month')
    def product_statistic_in_month(self, request, pk):
        try:
            user = User.objects.get(pk=request.user.id)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                product = Product.objects.get(pk=pk)
            except:
                return Response({"message": "product not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                month = request.query_params.get('month')
                year = request.query_params.get('year')
                order_details = OrderDetail.objects.filter(order__store=user, product_option__base_product=product)
                if month:
                    try:
                        month = int(month)
                    except:
                        return Response({"message": "month parameter was wrong format it must be [0-12]"})
                    else:
                        order_details = order_details.filter(order__order_date__month=month)
                else:
                    order_details = order_details.filter(order__order_date__month=timezone.now().month)
                if year:
                    try:
                        year = int(year)
                    except:
                        return Response({"message": "year parameter was wrong format it must be [0-9]"})
                    else:
                        order_details = order_details.filter(order__order_date__year=year).select_related()
                else:
                    order_details = order_details.filter(order__order_date__year=timezone.now().year).select_related()
                if order_details:
                    product_count_weekday = order_details.values('order__order_date__week_day') \
                        .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__week_day')
                    product_count_week = order_details.values('order__order_date__week') \
                        .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__week')
                    product_count_day = order_details.values('order__order_date__day') \
                        .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__day')
                    total_quantity_count = order_details.aggregate(total_quantity_count=Sum('quantity')).get(
                        'total_quantity_count')
                    return Response({
                        "product_count_weekday": list(product_count_weekday),
                        "product_count_week": list(product_count_week),
                        "product_count_day": list(product_count_day),
                        "total_quantity_count": total_quantity_count
                    }, status=status.HTTP_200_OK)
                return Response({"message": "order details not found"}, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 2))
    @action(methods=['get'], detail=True, url_path='product-statistic-in-year')
    def product_statistic_in_year(self, request, pk):
        try:
            user = User.objects.get(pk=request.user.id)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                product = Product.objects.get(pk=pk)
            except:
                return Response({"message": "product not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                year = request.query_params.get('year')
                order_details = OrderDetail.objects.filter(order__store=user, product_option__base_product=product)
            if year:
                try:
                    year = int(year)
                except:
                    return Response({"message": "month parameter was wrong format it must be [0-12]"})
                else:
                    order_details = order_details.filter(order__order_date__year=year).select_related()
            else:
                order_details = order_details.filter(order__order_date__year=timezone.now().year).select_related()
            if order_details:
                product_count_weekday = order_details.values('order__order_date__week_day') \
                    .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__week_day')
                product_count_week = order_details.values('order__order_date__week') \
                    .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__week')
                product_count_month = order_details.values('order__order_date__month') \
                    .annotate(total_product_count=Sum('quantity')).order_by('order__order_date__month')
                total_quantity_count = order_details.aggregate(total_quantity_count=Sum('quantity')).get(
                    'total_quantity_count')
                return Response({
                    "product_count_weekday": list(product_count_weekday),
                    "product_count_week": list(product_count_week),
                    "product_count_month": list(product_count_month),
                    "total_quantity_count": total_quantity_count
                }, status=status.HTTP_200_OK)
            return Response({"message": "order details not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True, url_path='vouchers-available')
    def get_vouchers_available_of_product(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response({"message": "product not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            vouchers = product.voucher_set.filter(Q(start_date__lte=timezone.now()) & (Q(end_date__gt=timezone.now()) | Q(end_date__isnull=True)))
            if vouchers:
                return Response(VoucherSerializer(vouchers, many=True).data)
            return Response({"message": "voucher not found"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        try:
            self.check_object_permissions(request, product)
        except:
            return Response({"message": "you do not have permission"}, status=status.HTTP_403_FORBIDDEN)
        order_id_list = product.option_set.filter(orderdetail__order__status=1)\
            .values_list("orderdetail__order__id", flat=True).distinct()
        if order_id_list:
            for i in order_id_list:
                cancel_order(i)
            Order.objects.filter(pk__in=order_id_list)
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    permission_classes = [permissions.AllowAny, ]

    def get_serializer_class(self):
        if self.action == 'get_category_vouchers_available':
            return VoucherSerializer
        return CategorySerializer

    @action(methods=['get'], detail=True, url_path="vouchers-available")
    def get_category_vouchers_available(self, request, pk):
        paginator = BasePagination()
        queryset = Voucher.objects.filter(Q(start_date__lte=timezone.now()) & (Q(end_date__gt=timezone.now()) | Q(end_date__isnull=True)) & Q(products__categories=pk))
        page = paginator.paginate_queryset(queryset, request)
        if page:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OptionViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    def get_permissions(self):
        if self.action == 'add_to_cart':
            return [permissions.IsAuthenticated(), ]
        return [BusinessPermission(), IsProductOptionOwner(), ]

    def get_serializer_class(self):
        if self.action == 'add_to_cart':
            return CartSerializer
        return OptionSerializer
    
    @action(methods=['post'], detail=True, url_path='add-to-cart')
    def add_to_cart(self, request, pk):
        try:
            op = Option.objects.get(pk=pk)
        except:
            return Response({"message": "option not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if op.base_product.owner.id == request.user.id:
                return Response({"message": "you are the product owner"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            cart = CartSerializer(data=request.data)
            if cart.is_valid(raise_exception=True):
                try:
                    cart.save(customer=request.user, product_option=op)
                except:
                    quantity = cart.validated_data.get('quantity')
                    with transaction.atomic():
                        cart_exist = CartDetail.objects.select_for_update().get(customer=request.user, product_option=op)
                        cart_exist.quantity = F('quantity') + quantity
                        cart_exist.save()
                    cart_exist = CartDetail.objects.get(customer=request.user, product_option=op)
                    return Response(CartSerializer(cart_exist).data)
                else:
                    return Response(cart.data)
            return Response({'message': 'cannot add product to your cart'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        option = self.get_object()
        try:
            self.check_object_permissions(request, option)
        except:
            return Response({"message": "you do not have permission"}, status=status.HTTP_403_FORBIDDEN)
        order_id_list = option.orderdetail_set.filter(order__status=1).values_list("order__id", flat=True)\
            .distinct()
        if order_id_list:
            for i in order_id_list:
                cancel_order(i)
            Order.objects.filter(pk__in=[order_id_list]).delete()
        return super().destroy(request, *args, **kwargs)


class OptionPictureViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Picture.objects.all()
    pagination_class = BasePagination
    permission_classes = [IsOptionPictureOwner, ]
    serializer_class = OptionPictureSerializer


class OrderViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveAPIView):
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'id', 'can_destroy', 'completed_date', 'order_date']
    ordering_fields = ['completed_date', 'order_date', 'bill__value']

    def get_permissions(self):
        if self.action in ["accept_order", "delete", "cancel_order"]:
            return [StoreOwnerPermission(), ]
        return [VerifiedUserPermission(), ]
        
    def get_serializer_class(self):
        if self.action in ["list"]:
            return ListOrderSerializer
        elif self.action == 'checkout':
            return CheckoutOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        orders = Order.objects.filter(Q(customer=self.request.user.id) | Q(store=self.request.user.id))
        state = self.request.query_params.get('state')
        if state:
            if state == '0':
                orders = orders.filter(customer=self.request.user.id)
            elif state == '1':
                orders = orders.filter(store=self.request.user.id)
        return orders

    def create(self, request, *args, **kwargs):
        if not request.user.address:
            return Response({'message': 'you need to add the address before make order'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.filter(customer=request.user.id, status=0)
        if order:
            order.delete()

        list_cart = request.data.get('list_cart')
        if list_cart:
            result = make_order_from_list_cart(list_cart_id=list_cart, user_id=request.user.id, data=request.data)
            if result:
                return Response(OrderSerializer(result, many=True).data, status=status.HTTP_201_CREATED)
            return Response({'message': 'wrong cart id, not found cart'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'you must add array of your cart id'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['get'], detail=False, url_path='cancel_uncheckout_order')
    def cancel_uncheckout_order(self, request):
        order = Order.objects.filter(customer=request.user.id, status=0)
        if order:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'not found uncheckout order'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='checkout_order')
    def checkout(self, request):
        order = Order.objects.filter(customer=request.user.id, status=0, bill__isnull=True)
        if order:
            voucher_code = request.data.get('list_voucher')
            result = []
            success = False
            payment_type = request.data.get('payment_type')
            try:
                for o in order:
                    m = None
                    voucher_code_order = None
                    if voucher_code is not None:
                        voucher_code_order = voucher_code.get(str(o.id))
                    if voucher_code_order is not None:
                        if payment_type:
                            m = checkout_order(order_id=o.id, voucher_code=voucher_code_order,
                                               payment_type=payment_type, raw_status=0)
                        else:
                            m = checkout_order(order_id=o.id, voucher_code=voucher_code_order)
                    else:
                        if payment_type:
                            m = checkout_order(order_id=o.id, payment_type=payment_type, raw_status=0)
                        else:
                            m = checkout_order(order_id=o.id)
                    if m is None:
                        raise Exception
                    result.append(m)
                success = True
            except:
                return Response({'message': 'some product options has out of stock or your balance not enough to pay'}, status=status.HTTP_400_BAD_REQUEST)
            if success:
                if not payment_type or (payment_type and payment_type != 1):
                    for i in result:
                        odds = i.orderdetail_set.values_list('cart_id__id', flat=True)
                        CartDetail.objects.filter(id__in=list(set(odds))).delete()
                        subject = "B???n c?? 1 ????n h??ng m???i ch??? x??c nh???n"
                        content = f"????n h??ng {i.id} gi?? tr??? {i.bill.value}vn?? ??ang ch??? b???n x??c nh???n ????? ???????c v???n chuy???n"
                        send_email_task.delay(i.customer.email, subject, content)
                        #### WebSocket ####
                        try:
                            channel = i.store.client
                            message = {
                                "status": i.status,
                                "order_id": i.id
                            }
                            send_message_to_channel.delay(channel_name=channel.channel_name, message=message)
                        except:
                            pass
                        ########
                elif payment_type and payment_type == 1:
                    list_id = [x.id for x in result]
                    instance = import_signature(list_id)
                    return Response({"message": "Please pay with the link to complete checkout the order",
                                     "pay_url": instance.get("payUrl")}, status=status.HTTP_201_CREATED)

                return Response(OrderSerializer(result, many=True).data, status=status.HTTP_202_ACCEPTED)
            return Response({'message': 'can not checkout the orders'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message': 'can not found the orders uncheckout'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True, url_path='accept_order')
    def accept_order(self, request, pk):
        try:
            order = Order.objects.select_related().get(pk=pk)
        except Order.DoesNotExist:
            return Response({'message': 'order not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            self.check_object_permissions(request, order)
        except:
            return Response({'message': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        if order.status != 1:
            return Response({'message': 'order not approving'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if update_shipping_code(order_id=order.id):
            order.refresh_from_db()
            subject = "NightOwl - ????n h??ng {0} c???a b???n ??ang ???????c v???n chuy???n".format(order.id)
            content = """????n h??ng {0} ??ang ???????c v???n chuy???n b???i ng?????i b??n, qu?? kh??ch vui l??ng ch??? shipper giao h??ng t???i nh??.
                Ho???c b???n c?? th??? ki???m tra t??nh tr???ng ????n h??ng v???i m?? ????n h??ng l?? {1} ???????c v???n chuy???n b???i ????n v??? Giaohangnhanh.
                Night Owl ECommerce xin c???m ??n qu?? kh??ch ???? tin t?????ng l???a ch???n.""".format(order.id, order.shipping_code)
            #### WebSocket ####
            try:
                channel = order.customer.client
                message = {
                    "status": order.status,
                    "order_id": order.id,
                    "subject": subject,
                    "content": content
                }
                send_message_to_channel.delay(channel_name=channel.channel_name, message=message)
            except:
                pass
            ########
            send_email_task.delay(order.customer.email, subject, content)
            # y = Thread(target=send_sms, args=(order.customer.phone_number, content))
            # y.start()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response({'message': 'failed to create shipping order'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='cancel_order')
    def cancel_order(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, status=1)
        except Order.DoesNotExist:
            return Response({'message': 'order not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            self.check_object_permissions(request, order)
        except:
            return Response({'message': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if cancel_order(order.id):
                subject = "????n h??ng {0} c???a b???n ???? b??? h???y".format(order.id)
                content = """Ng?????i b??n ???? h???y ????n h??ng {0} c???a b???n, n???u b???n s??? d???ng ph????ng th???c thanh to??n tr???c tuy???n b???n vui l??ng 
                ki???m tra l???i t??i kho???n ???? thanh to??n {1}vn?? xem ???? ???????c h??? th???ng ho??n ti???n l???i hay ch??a.
                N???u ch??a b???n vui l??ng g???i report ????? ???????c h??? tr??? s???m nh???t.""".format(order.id, order.bill.value)
                #### WebSocket ####
                try:
                    channel = order.customer.client
                    message = {
                        "status": order.status,
                        "order_id": order.id,
                        "subject": subject,
                        "content": content
                    }
                    send_message_to_channel.delay(channel_name=channel.channel_name, message=message)
                except:
                    pass
                ########
                send_email_task.delay(order.customer.email, subject, content)
                # y = Thread(target=send_sms, args=(order.customer.phone_number, content))
                # y.start()
                return Response({"message": "order canceled", "order_id": order.id}, status=status.HTTP_200_OK)
            return Response({"message": "can not cancel order"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path="recieve_order")
    def receive_order(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, status=2)
        except:
            return Response({"message": "order not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            self.check_object_permissions(request, order)
        except:
            return Response({'message': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if receive_order(order.id):
                subject = "????n h??ng {0} ???? ???????c giao th??nh c??ng".format(order.id)
                content = """Ng?????i mua ???? nh???n ???????c ????n h??ng {0} gi?? tr??? {1}vn?? , b???n vui l??ng ki???m tra t??nh tr???ng ????n h??ng.
                N???u c?? sai s??t b???n vui l??ng g???i report cho d???ch v??? h??? tr??? c???a Night Owl s???m nh???t ????? ???????c x??? l??.
                Xin c???m ??n b???n ???? tin t?????ng ch???n Nigh Owl ECommerce l??m ?????i t??c b??n h??ng.""".format(order.id, order.bill.value)
                #### WebSocket ####
                try:
                    channel = order.store.client
                    message = {
                        "status": order.status,
                        "order_id": order.id,
                        "subject": subject,
                        "content": content
                    }
                    send_message_to_channel.delay(channel_name=channel.channel_name, message=message)
                except:
                    pass
                ########
                send_email_task.delay(order.store.email, subject, content)
                # y = Thread(target=send_sms, args=(order.store.phone_number, content))
                # y.start()
                return Response({'message': 'order completed'}, status=status.HTTP_200_OK)
            return Response({'message': 'something problem so we can not change the order status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='voucher-available')
    def get_voucher_available(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except:
            return Response({"message": "order not found"}, status=status.HTTP_404_NOT_FOUND)
        options = order.orderdetail_set.all().values_list('product_option', flat=True)
        vouchers = Voucher.objects.filter(products__option__in=options)\
            .filter(Q(start_date__lte=timezone.now()) & (Q(end_date__gt=timezone.now()) | Q(end_date__isnull=True)))
        if vouchers:
            return Response(VoucherSerializer(vouchers, many=True).data, status=status.HTTP_200_OK)
        return Response({"message": "voucher not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderDetailViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [VerifiedUserPermission]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        ordd = OrderDetail.objects.filter(Q(order__customer__id=self.request.user.id) |
                                          Q(order__store__id=self.request.user.id))
        if status:
            ordd.filter(order__status=status)
        return ordd


class BillViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    pagination_class = ProductPagination
    permission_classes = [VerifiedUserPermission]

    def get_permissions(self):
        if self.action in ['monthly_statistic', ]:
            return [BusinessPermission(),]
        return super().get_permissions()

    @method_decorator(cache_page(60 * 60 * 2))
    @action(methods=['get'], detail=False, url_path='yearly-value-statistic')
    def yearly_statistic(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            year = request.query_params.get('year')
            order = Order.objects.exclude(status=0).filter(store__id=user.id)
            if year:
                try:
                    year = int(year)
                except:
                    return Response({"message": "year parameter was wrong format"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    order = order.filter(order_date__year=year).select_related()
            else:
                order = order.filter(order_date__year=timezone.now().year).select_related()
            if order:
                order_weekday = order.values('order_date__week_day')\
                    .annotate(total_value=Sum('bill__value'), total_count=Count('id')).order_by('order_date__week_day')
                order_week = order.values('order_date__week')\
                    .annotate(total_value=Sum('bill__value'), total_count=Count('id')).order_by('order_date__week')
                order_month = order.values('order_date__month')\
                    .annotate(total_value=Sum('bill__value'), total_count=Count('id')).order_by('order_date__month')
                total_order_value = order.aggregate(total_value=Sum('bill__value')).get('total_value')
                return Response({
                    "weekday": list(order_weekday),
                    "week": list(order_week),
                    "month": list(order_month),
                    "orders_total_value": total_order_value,
                    "orders_total_count": order.count()
                }, status=status.HTTP_200_OK)
            return Response({"message": "orders not found"}, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 2))
    @action(methods=['get'], detail=False, url_path='monthly-value-statistic')
    def monthly_statistic(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            month = request.query_params.get('month')
            year = request.query_params.get('year')
            order = Order.objects.exclude(status=0).filter(store__id=user.id)
            if year:
                try:
                    year = int(year)
                except:
                    return Response({"message": "year parameter was wrong format"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    order = order.filter(order_date__year=year)
            else:
                order = order.filter(order_date__year=timezone.now().year)
            if month:
                try:
                    month = int(month)
                except:
                    return Response({"message": "month parameter was wrong format"}, status=status.HTTP_400_BAD_REQUEST)
                order = order.filter(order_date__month=month).select_related()
            else:
                order = order.filter(order_date__month=timezone.now().month).select_related()
            if order:
                order_weekday = order.values('order_date__week_day')\
                    .annotate(total_value=Sum('bill__value'), total_count=Count('id')).order_by('order_date__week_day')
                order_week = order.values('order_date__week')\
                    .annotate(total_value=Sum('bill__value'), total_count=Count('id')).order_by('order_date__week')
                order_day = order.values('order_date__day')\
                    .annotate(total_value=Sum('bill__value'), total_count=Count('id')).order_by('order_date__day')
                total_order_value = order.aggregate(total_value=Sum('bill__value')).get('total_value')
                return Response({
                    "weekday": list(order_weekday),
                    "week": list(order_week),
                    "day": list(order_day),
                    "orders_total_value": total_order_value,
                    "orders_total_count": order.count()
                }, status=status.HTTP_200_OK)
            return Response({"message": "orders not found"}, status=status.HTTP_404_NOT_FOUND)


class RoomViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    queryset = Room.objects.all().order_by('updated_date')
    serializer_class = RoomSerializer
    pagination_class = CommentPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        rooms = Room.objects.filter(user__in=[self.request.user.id]).annotate(latest=Max('message__created_date')).order_by('-latest')
        return rooms

    def get_serializer_class(self):
        if self.action in ["send_message_to_room", "get_room_messages"]:
            return ChatRoomMessageSerialier
        return RoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data, context={'user': request.user.id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "can not create room"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"user": request.user.id})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"user": request.user.id})
        return Response(serializer.data)

    @action(methods=['patch'], detail=True, url_path='add-member')
    def add_member_to_chatroom(self, request, pk):
        try:
            room = Room.objects.get(pk=pk, room_type=1)
        except:
            return Response({"message": "room not found"}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(pk=request.user.id)
        if user and room.user.filter(pk=user.id).exists():
            list_user_ids = request.data.get('list_user_ids')
            list_users = User.objects.filter(id__in=list_user_ids)
            if list_users:
                room.user.add(*list_users)
                return Response(RoomSerializer(room).data)
            return Response({"message": "list user not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "you do not have permission"}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['delete'], detail=True, url_path='delete-chatroom')
    def delete_chat_room(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
        except:
            return Response({"message": "room not found"}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(pk=request.user.id)
        if user and room.user.filter(pk=user.id).exists():
            room.user.remove(user)
            return Response({"message": "room deleted for you"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "you do not have permission"}, status=status.HTTP_403_FORBIDDEN)

    @method_decorator(cache_page(60 * 60 * 2))
    @action(methods=['get'], detail=True, url_path='messages')
    def get_room_messages(self, request, pk):
        queryset = Message.objects.filter(room__pk=pk).order_by('-created_date')
        paginator = BasePagination()
        page = paginator.paginate_queryset(queryset, request)
        if page:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Message.objects.all().order_by('-created_date')
    serializer_class = ChatRoomMessageSerialier
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['room__id']

    def get_queryset(self):
        return Message.objects.filter(room__user=self.request.user).order_by('-created_date')

    def list(self, request, *args, **kwargs):
        room_id = request.query_params.get('room__id')
        if room_id is None:
            return Response({"message": "room__id is  required"}, status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, *args, **kwargs)


class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        if self.action == 'get_available_vouchers':
            return Voucher.objects.filter(Q(start_date__lte=timezone.now()) & (Q(end_date__gt=timezone.now()) | Q(end_date__isnull=True)))
        return Voucher.objects.all()

    def create(self, request, *args, **kwargs):
        can_add = False
        # Check night owl staff
        if request.user and request.user.is_staff:
            can_add = True
        else:
            products = Product.objects.filter(owner=request.user.id, id__in=[o for o in request.data.get('products')])
            # Check product owner in list product
            if list(products.values_list('id', flat=True)) == request.data.get('products'):
                can_add = True
        if can_add:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(creator=request.user)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return Response({'message': 'can not create voucher'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'can not add voucher to product that you are not the owner'},
                        status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=False, url_path='available')
    def get_available_vouchers(self, request):
        return super().list(request)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_available_vouchers']:
            return [permissions.AllowAny(), ]
        elif self.action == 'create':
            return [BusinessPermission(), ]
        return [BusinessPermission(), IsCreator(), ]


class ReportViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerialier
    permission_classes = [permissions.IsAuthenticated, IsReporter]
    pagination_class = BasePagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(reporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "some thing not correct, please create report again"},\
                        status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        reports = Report.objects.prefetch_related('reply_set').filter(reporter=self.request.user.id)
        return reports

    def get_serializer_class(self):
        if self.action == 'add_reply_to_report':
            return ReplySerializer
        elif self.action == 'list':
            return ListReportSerializer
        return ReportSerialier

    @action(methods=['post'], detail=True, url_path='add-reply')
    def add_reply_to_report(self, request, pk):
        try:
            report = Report.objects.get(pk=pk)
        except:
            return Response({"message": "report not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            self.check_object_permissions(request, report)
        except:
            return Response({"message": "you do not have permission"}, status=status.HTTP_403_FORBIDDEN)
        if report.status == 3:
            return Response({"message": "report had been done, please create new report to add reply"}, status=status.HTTP_410_GONE)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(creator=request.user, report=report)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "something wrong"}, status=status.HTTP_400_BAD_REQUEST)


class MomoPayedView(APIView):
    def post(self, request, secret_link):
        try:
            orderId = request.data.get('orderId')
            requestId = request.data.get('requestId')
            resultCode = request.data.get('resultCode')
            transId = request.data.get('transId')
            amount = request.data.get('amount')

        except:
            pass
        else:
            instance = get_instance_from_signature_and_request_id(secret_link=secret_link, orderId=orderId, requestId=requestId)
            momo_order = check_momo_order_status(order_id=orderId, request_id=requestId)
            if instance and momo_order.get('amount') == amount == instance.get('amount') and momo_order.get('resultCode') == resultCode == 0:
                if instance.get("type") == 0:
                    order_ids = instance.get('order_ids')
                    if not complete_checkout_orders_with_payment_gateway(order_ids):
                        x = Thread(target=momo_refund, args=(transId, amount, requestId))
                        x.start()
                else:
                    increase_user_balance(instance.get("user_id"), amount)
        finally:
            return Response(status=status.HTTP_204_NO_CONTENT)
