from rest_framework.routers import SimpleRouter

from payment.views import PaymentAccountViewSet

app_name = 'api'

router = SimpleRouter()
router.register(r'', PaymentAccountViewSet)

urlpatterns = router.urls
