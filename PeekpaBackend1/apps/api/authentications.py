from rest_framework_simplejwt.tokens import BlacklistMixin, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class PassGetAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        token = header[len("Bearer "):]
        # Token 长度为0，则返回 None，验证失败
        if token is None or len(token) == 0:
            return None
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        try:
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken as e:
            if request.method == 'GET':
                return None, None
            else:
                raise e

        user = self.get_user(validated_token)
        # 如果用户存在且为公司员工，返回用户和验证后的 Token
        if user and user.is_staff:
            return user, validated_token
        # 如果用户存在，则返回用户和验证后的 Token
        elif user:
            return user, validated_token
        # 如果请求方法是 GET，则返回 None, None，表示匿名用户和无效 Token
        if request.method == 'GET':
            return None, None
        # 对于其他请求方法，返回 None，表示身份验证失败
        return None

class PeekpaAccessToken(BlacklistMixin, AccessToken):
    token_type = "access"

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        # 添加自定义内容
        token['is_staff'] = user.is_staff
        token['email'] = user.email
        token['name'] = user.name
        if 'company_id' in user.details:
            token['is_manager'] = user.details.get('is_manager', False)
        if user.is_superuser:
            token['is_superuser'] = user.is_superuser
        return token