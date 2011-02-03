from django.template.response import TemplateResponse

from ..products.models import Product
from ..static import testcyclestatus
from ..users.decorators import login_required

from .models import TestCycleList



@login_required
def cycles(request, product_id):
    product = Product.get("products/%s" % product_id, auth=request.auth)

    cycles = TestCycleList.get(auth=request.auth).filter(
        productId=product_id, testCycleStatusId=testcyclestatus.ACTIVE)

    return TemplateResponse(
        request, "test/cycles.html", {"product": product, "cycles": cycles})
