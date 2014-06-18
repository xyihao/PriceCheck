from django.shortcuts import render
from products.models import Products,SKU


def searchProduct(request):
	show_product=False
	if 'query' in request.GET and request.GET['query']:
		query=request.GET['query']
		words=query.split(',')
		result=SKU.objects.filter(name__contains=unicode(words[0]))
		for word in words[1:]:
			if len(result)==0:
				break
			result=result.filter(name__contains=unicode(word))
		product_num=len(result)
		show_product=True
		return render(request,'searchPage.html',{'product_num':product_num,'items':result,'show_product':show_product,'query':query})
	return render(request,'searchPage.html',{'show_product':show_product,})



# Create your views here.
