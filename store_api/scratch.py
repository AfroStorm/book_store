""" class CategorySerializer(serializers.ModelSerializer):
    '''
    Serializes the category models.
    '''
    class Meta:
        model = models.Category
        fields = ['name']
        extra_kwargs = {
            'name': {'read_only': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    '''
    Serializes the product model
    '''
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='caption'
    )
    category = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = models.Product
        fields = '__all__'
        read_only_fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Serializes the profile
    '''

    class Meta:
        model = models.Profile
        fields = [
            'id', 'address', 'last_login', 'date_joined', 'customer',
            'purchase_history', 'wishlist'
        ]
        extra_kwargs = {
            'purchase_history': {'read_only': True},
            'customer': {'read_only': True}
        }
 """
